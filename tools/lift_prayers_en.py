# -*- coding: utf-8 -*-
"""The English prayers come out of the calendar.

PRAYERS was 241 KB of index.html and 213 KB of that is the prayer text
itself, carried by every reader whether he ever opened the prayer panel or
not. Twenty-one languages already read theirs from
data/prayers-i18n.v2.<lang>.json; English was the exception only because it
was the language the page was written in.

What stays in the page is what the panel needs to draw its list before
anything is fetched: the category, the title and the hour. The text arrives
when the panel is opened, which is the same moment a Russian reader's text
arrives today.

    python3 tools/lift_prayers_en.py --file     # ship it, confirm it
    python3 tools/lift_prayers_en.py --point    # then turn the page over
"""
import io, json, os, sys

PAGE = "index.html"
OUT = os.path.join("data", "prayers-i18n.v2.en.json")
HEAD = "const PRAYERS="
KEEP = ("cat", "title", "hour")
MOVE = ("title", "body", "note", "src")


def span(src):
    i = src.index(HEAD)
    j = src.index("\n", i)
    return i + len(HEAD), j


def write_file(src):
    a, b = span(src)
    prayers = json.loads(src[a:b].rstrip().rstrip(";"))
    out = {}
    for p in prayers:
        out[p["title"]] = dict((k, p.get(k, "")) for k in MOVE)
    io.open(OUT, "w", encoding="utf-8").write(
        json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    print("%s: %d prayers, %.0f KB"
          % (OUT, len(out), os.path.getsize(OUT) / 1024.0))


SUBS = [
 # English is fetched like the other twenty-one
 ('function loadPrayerLang(L,cb){if(!L||L==="en"||PRAYERS_I18N[L]){if(cb)cb();return;}',
  'function loadPrayerLang(L,cb){if(!L||PRAYERS_I18N[L]){if(cb)cb();return;}'),
 # a language landing changes what the search can see
 ('.then(function(j){if(j)PRAYERS_I18N[L]=j;})',
  '.then(function(j){if(j){PRAYERS_I18N[L]=j;_sidx=null;}})'),
 # English is the base the others fall back to, wherever it has got to
 ('function prayTr(p){const o=(PRAYERS_I18N[lang]&&PRAYERS_I18N[lang][p.title])||null;'
  'return {enTitle:p.title,title:(o&&o.title)||p.title,body:(o&&o.body)||p.body,'
  'note:(o&&o.note!==undefined)?o.note:(lang==="en"?p.note:""),'
  'src:(o&&o.src)?o.src:(lang==="en"?p.src:"")};}',
  'function prayTr(p){const o=(PRAYERS_I18N[lang]&&PRAYERS_I18N[lang][p.title])||null;'
  'const b=(PRAYERS_I18N.en&&PRAYERS_I18N.en[p.title])||p;'
  'return {enTitle:p.title,title:(o&&o.title)||b.title||p.title,body:(o&&o.body)||b.body||"",'
  'note:(o&&o.note!==undefined)?o.note:(lang==="en"?(b.note||""):""),'
  'src:(o&&o.src)?o.src:(lang==="en"?(b.src||""):"")};}'),
 # and the search reads it from there too
 ('PRAYERS.forEach((p,i)=>{let hay=p.title+" "+p.body+" "+(p.cat||"")+" ";',
  'PRAYERS.forEach((p,i)=>{const _pb=(PRAYERS_I18N.en&&PRAYERS_I18N.en[p.title])||p;'
  'let hay=p.title+" "+(_pb.body||"")+" "+(p.cat||"")+" ";'),
 # opening the panel asks for both, and each repaints as it lands
 ('function openPrayPanel(){prayScrollPos=0;renderPrayIndex();renderPrayExtras();'
  'showPrayList();$("prayov").hidden=false;'
  'loadPrayerLang(lang,function(){renderPrayIndex();renderPrayExtras();});}',
  'function openPrayPanel(){prayScrollPos=0;renderPrayIndex();renderPrayExtras();'
  'showPrayList();$("prayov").hidden=false;'
  'var _rp=function(){renderPrayIndex();renderPrayExtras();};'
  'loadPrayerLang("en",_rp);loadPrayerLang(lang,_rp);}'),
]


def point(src):
    if not os.path.exists(OUT):
        raise SystemExit("%s is not there; run --file first" % OUT)
    a, b = span(src)
    prayers = json.loads(src[a:b].rstrip().rstrip(";"))
    have = json.load(io.open(OUT, encoding="utf-8"))
    missing = [p["title"] for p in prayers
               if not (have.get(p["title"], {}).get("body") or "").strip()]
    if missing:
        raise SystemExit("%d prayers have no text in the file: %s"
                         % (len(missing), ", ".join(missing[:3])))
    slim = [dict((k, p[k]) for k in KEEP if k in p) for p in prayers]
    src = (src[:a] + json.dumps(slim, ensure_ascii=False, separators=(",", ":"))
           + ";" + src[b:])
    for old, new in SUBS:
        if new in src:
            continue
        if old not in src:
            raise SystemExit("not found: " + old[:70])
        src = src.replace(old, new, 1)
    return src, len(prayers)


def main():
    src = io.open(PAGE, encoding="utf-8").read()
    if "--file" in sys.argv:
        write_file(src)
    elif "--point" in sys.argv:
        a, b = span(src)
        before = b - a
        out, n = point(src)
        a2, b2 = span(out)
        print("%s: %d prayers, PRAYERS %.0f KB -> %.0f KB"
              % (PAGE, n, before / 1024.0, (b2 - a2) / 1024.0))
        io.open(PAGE, "w", encoding="utf-8").write(out)
    else:
        a, b = span(src)
        print("%.0f KB of PRAYERS in the page" % ((b - a) / 1024.0))


if __name__ == "__main__":
    main()
