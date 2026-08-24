# -*- coding: utf-8 -*-
"""Which Churches' saints the calendar shows.

The scope control had two settings: this Church, or all of them. All of them
meant every local commemoration on the site poured into one list with nothing
to say who kept which, and there was no way to ask for two Churches rather
than one or ten. A reader with a Serbian mother and a Romanian parish had to
choose which half of his family the calendar was for.

So: a third setting, and a row of the Churches to tick. Every local
commemoration now carries the Church that keeps it and says so on the line,
which also retires the untranslated word "local" that stood there before.

    python3 tools/saints_scope.py --write
"""
import io, json, re, subprocess, sys

PATH = "index.html"

# --- 1. two words, in the twenty-two -----------------------------------------

UI = {
 "someChurches": {
  "en": u"Choose",   "el": u"Επιλογή",  "ru": u"Выбрать", "ro": u"Alege",
  "uk": u"Вибрати",  "de": u"Auswahl",  "es": u"Elegir",  "ar": u"اختيار",
  "fr": u"Choisir",  "pt": u"Escolher", "it": u"Scegli",  "sr": u"Избор",
  "ka": u"არჩევა",   "zh": u"选择",      "ja": u"選択",     "ko": u"선택",
  "sw": u"Chagua",   "hy": u"Ընտրել",   "arc": u"ܓܒܝܬܐ",  "hi": u"चुनें",
  "bn": u"বেছে নিন", "ur": u"منتخب کریں"},
 "churchesShown": {
  "en": u"Churches shown",          "el": u"Εκκλησίες που εμφανίζονται",
  "ru": u"Показанные Церкви",       "ro": u"Bisericile afișate",
  "uk": u"Показані Церкви",         "de": u"Angezeigte Kirchen",
  "es": u"Iglesias mostradas",      "ar": u"الكنائس المعروضة",
  "fr": u"Églises affichées",       "pt": u"Igrejas mostradas",
  "it": u"Chiese mostrate",         "sr": u"Приказане Цркве",
  "ka": u"ნაჩვენები ეკლესიები",     "zh": u"显示的教会",
  "ja": u"表示する教会",              "ko": u"표시된 교회",
  "sw": u"Makanisa yanayoonyeshwa", "hy": u"Ցուցադրվող եկեղեցիները",
  "arc": u"ܥܕܬܐ ܕܡܬܚܙܝܢ",           "hi": u"दिखाए गए चर्च",
  "bn": u"প্রদর্শিত চার্চসমূহ",        "ur": u"دکھائے گئے کلیسیا"},
}

# --- 2. the scope itself -----------------------------------------------------

# One function per line, and the two tables they read sit between them, so
# each is taken on its own rather than as one run.
OLD_DEDUPE = [
    re.compile(r"^function dedupeLocal\(\)\{.*\n", re.M),
    re.compile(r"^function dedupeLocalMovable\(\)\{.*\n", re.M),
    re.compile(r"^function dedupeLocalCivil\(\)\{.*\n", re.M),
]

NEW_SCOPE = u'''/* Which Churches' own commemorations are shown. One, all of them, or the
   few a reader actually keeps. Each entry carries the Church it came from,
   so a day that shows six saints can say who keeps which. */
function scopeKeys(){
  if(saintsScope==="church")return [juris];
  const all=Object.keys(JURISDICTIONS);
  if(saintsScope==="some"){const k=all.filter(x=>saintsPick.has(x));return k.length?k:[juris];}
  return all;
}
function localsFrom(tbl,key){
  const out=[],seen=new Set();
  for(const j of scopeKeys())for(const f of (tbl[j]||[])){
    const k=key(f);if(seen.has(k))continue;seen.add(k);out.push(Object.assign({},f,{j:j}));}
  return out;
}
function dedupeLocal(){return localsFrom(LOCAL_FIXED,f=>f.mo+"-"+f.da+f.name.slice(0,12));}
function dedupeLocalMovable(){return localsFrom(LOCAL_MOVABLE,m=>m.off+"|"+m.name);}
function dedupeLocalCivil(){return localsFrom(LOCAL_CIVIL,m=>m.mo+"|"+m.dow+"|"+m.nth+"|"+m.name);}
'''

# commemsFor: the three lines that chose between one Church and all of them
SUBS = [
 ('{const decl=(saintsScope==="all")?null:(OMIT_FIXED[juris]||null);',
  '{const _sk=scopeKeys();const decl=(_sk.length===1)?(OMIT_FIXED[_sk[0]]||null):null;'),
 ('const isAll = saintsScope==="all";\n  const locals = isAll ? dedupeLocal() : (LOCAL_FIXED[juris]||[]);',
  '/* A Church renames a base commemoration for itself - Vladimir into\n'
  '     Volodymyr - and that only makes sense while one Church is in scope. */\n'
  '  const isAll = scopeKeys().length!==1;\n  const locals = dedupeLocal();'),
 ('const lmovs = saintsScope==="all" ? dedupeLocalMovable() : (LOCAL_MOVABLE[juris]||[]);',
  'const lmovs = dedupeLocalMovable();'),
 ('const lcivs = saintsScope==="all" ? dedupeLocalCivil() : (LOCAL_CIVIL[juris]||[]);',
  'const lcivs = dedupeLocalCivil();'),
 ('for(const m of lmovs){ if(m.off===off) out.push({name:m.name,great:false,local:true,cal:""}); }',
  'for(const m of lmovs){ if(m.off===off) out.push({name:m.name,great:false,local:true,j:m.j,cal:""}); }'),
 ('for(const m of lcivs){ if(d.getMonth()===m.mo-1 && d.getDay()===m.dow && Math.ceil(d.getDate()/7)===m.nth) out.push({name:m.name,great:false,local:true,cal:""}); }',
  'for(const m of lcivs){ if(d.getMonth()===m.mo-1 && d.getDay()===m.dow && Math.ceil(d.getDate()/7)===m.nth) out.push({name:m.name,great:false,local:true,j:m.j,cal:""}); }'),
 ('if(bi>=0){out[bi]={...out[bi],name:f.name,local:true};}else{out.push({...f,great:false,local:true,cal:""});}}else{out.push({...f,great:false,local:true,cal:""});}}',
  'if(bi>=0){out[bi]={...out[bi],name:f.name,local:true,j:f.j};}else{out.push({...f,great:false,local:true,cal:""});}}else{out.push({...f,great:false,local:true,cal:""});}}'),
 # the line under a commemoration names the Church rather than saying "local"
 ('if(c.local)b+=\' <span style="font-family:var(--mono);font-size:9.5px;color:var(--muted)">\\u00b7 local</span>\';',
  'if(c.local)b+=\' <span style="font-family:var(--mono);font-size:9.5px;color:var(--muted)">\\u00b7 \'+sEsc(c.j?t("jz_"+c.j):t("thisChurch"))+\'</span>\';'),
 # the state itself
 ('let juris="greek", mode=JURISDICTIONS.greek.cal, rite=JURISDICTIONS.greek.rite, saintsScope="church",',
  'let juris="greek", mode=JURISDICTIONS.greek.cal, rite=JURISDICTIONS.greek.rite, saintsScope="church", saintsPick=new Set(Object.keys(JURISDICTIONS)),'),
]

# --- 3. the control ----------------------------------------------------------

BTN_OLD = ('<button data-s="all" data-i18n="allSaints" aria-pressed="false">All saints</button>\n'
           '    </div>')
BTN_NEW = ('<button data-s="all" data-i18n="allSaints" aria-pressed="false">All saints</button>'
           '<button data-s="some" data-i18n="someChurches" aria-pressed="false">Choose</button>\n'
           '    </div>\n'
           '    <div class="jpick" id="jpick" hidden></div>')

CSS_ANCHOR = '.seg button[aria-pressed="true"]'
CSS_ADD = ('.jpick{flex-basis:100%;display:flex;flex-wrap:wrap;gap:6px;margin:2px 0 0}'
           '.jpick[hidden]{display:none}'
           '.jpick button{font-family:var(--mono);font-size:10px;letter-spacing:.05em;'
           'text-transform:uppercase;padding:5px 9px;border:1px solid var(--rule);'
           'border-radius:2px;background:var(--leaf);color:var(--ink-soft);cursor:pointer}'
           '.jpick button[aria-pressed="true"]{background:var(--porphyry);color:#f6f1ee;'
           'border-color:var(--porphyry)}'
           '.jpick button:focus-visible{outline:2px solid var(--porphyry);outline-offset:1px}')

WIRE_OLD = ('$("saints").querySelectorAll("button").forEach(b=>b.onclick=()=>{saintsScope=b.dataset.s;'
            '$("saints").querySelectorAll("button").forEach(x=>x.setAttribute("aria-pressed",String(x===b)));renderAll();});')

WIRE_NEW = u'''$("saints").querySelectorAll("button").forEach(b=>b.onclick=()=>{saintsScope=b.dataset.s;
  $("saints").querySelectorAll("button").forEach(x=>x.setAttribute("aria-pressed",String(x===b)));
  paintPick();renderAll();});
/* The row of Churches to tick, shown only when the reader has asked to choose.
   It is redrawn on a language change so the names follow the page. */
function paintPick(){
  const p=$("jpick");if(!p)return;
  p.hidden=(saintsScope!=="some");
  p.setAttribute("role","group");
  p.setAttribute("aria-label",t("churchesShown"));
  if(p.hidden){p.innerHTML="";return;}
  p.innerHTML=Object.keys(JURISDICTIONS).map(function(k){
    return '<button type="button" data-j="'+k+'" aria-pressed="'+(saintsPick.has(k)?"true":"false")+'">'+sEsc(t("jz_"+k))+'</button>';
  }).join("");
  p.querySelectorAll("button").forEach(function(b){b.onclick=function(){
    const k=b.dataset.j;
    if(saintsPick.has(k))saintsPick.delete(k);else saintsPick.add(k);
    b.setAttribute("aria-pressed",saintsPick.has(k)?"true":"false");
    renderAll();};});
}'''


I18N_OLD = ('function applyI18n(){if(typeof LANG_NAMES==="object"&&LANG_NAMES'
            '&&!LANG_NAMES[lang])lang="en";updateBrand();')
I18N_NEW = I18N_OLD + 'if(typeof paintPick==="function")paintPick();'


def js_object(src, decl):
    """The literal that follows a `const NAME=` declaration, as a slice."""
    i = src.index(decl)
    k = i + len(decl)
    while src[k] not in "{[":
        k += 1
    a = k
    d = 0
    instr = False
    q = ""
    esc = False
    while k < len(src):
        c = src[k]
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == q:
                instr = False
            k += 1
            continue
        if c in "\"'`":
            instr = True
            q = c
            k += 1
            continue
        if c in "{[":
            d += 1
        elif c in "}]":
            d -= 1
            if d == 0:
                return a, k + 1
        k += 1
    raise SystemExit(decl + ": unbalanced")


def add_ui(src):
    a, b = js_object(src, "const I18N=")
    io.open("/tmp/i18n.js", "w", encoding="utf-8").write(
        u"require('fs').writeFileSync('/tmp/i18n.json',JSON.stringify(%s));" % src[a:b])
    subprocess.check_call(["node", "/tmp/i18n.js"])
    table = json.load(io.open("/tmp/i18n.json", encoding="utf-8"))
    n = 0
    for key, words in UI.items():
        for lang, word in words.items():
            if lang in table and key not in table[lang].get("ui", {}):
                table[lang].setdefault("ui", {})[key] = word
                n += 1
    return (src[:a] + json.dumps(table, ensure_ascii=False, separators=(",", ":")) + src[b:], n)


def main():
    src = io.open(PATH, encoding="utf-8").read()
    if "function scopeKeys()" in src:
        print("already installed")
        return

    src, n = add_ui(src)

    # Take all three out first and only then put the replacement in. Done the
    # other way round the second and third patterns match the functions inside
    # NEW_SCOPE, which have the same names, and delete those instead.
    cuts = []
    for n, rx in enumerate(OLD_DEDUPE):
        m = rx.search(src)
        if not m:
            raise SystemExit("dedupe function %d was not found" % n)
        cuts.append((m.start(), m.end()))
    for i, (lo, hi) in enumerate(reversed(cuts)):
        src = src[:lo] + (NEW_SCOPE if len(cuts) - 1 - i == 0 else "") + src[hi:]

    for old, new in SUBS:
        if old not in src:
            raise SystemExit("not found: " + old[:70])
        src = src.replace(old, new, 1)

    for old, new in ((BTN_OLD, BTN_NEW), (WIRE_OLD, WIRE_NEW), (I18N_OLD, I18N_NEW)):
        if old not in src:
            raise SystemExit("not found: " + old[:70])
        src = src.replace(old, new, 1)

    src = src.replace(CSS_ANCHOR, CSS_ADD + CSS_ANCHOR, 1)

    if "--write" in sys.argv:
        io.open(PATH, "w", encoding="utf-8").write(src)
        print("wrote %s: %d words added, scope rewritten" % (PATH, n))
    else:
        print("would write: %d words added, scope rewritten" % n)


if __name__ == "__main__":
    main()
