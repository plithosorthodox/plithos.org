# -*- coding: utf-8 -*-
"""Every reading the calendar prints must be a passage the site can show.

The Western-rite lectionary cites eighteen Old Testament books. They were
inside index.html and loadBibleEn threw them away on every load, so every one
of those readings was dead - not a link, no text - and nothing failed. Only a
browser with the fetch held back showed it.

So this asks the question the page asks: walk the Western rite and the
Byzantine day through several years, take every epistle and gospel reference
the tables produce, and confirm each one parses and resolves to at least one
verse against data/bible-en.v2.json. A reference that names a book the file
does not carry is an error; one that parses but yields nothing is listed for
review, because the editions are cited chapter by chapter and a gap may be
deliberate.

    python3 tools/check_lectionary.py
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "index.html")
BIBLE = os.path.join(ROOT, "data", "bible-en.v2.json")

HARNESS = r"""
const fs=require("fs");
const src=fs.readFileSync(PAGE,"utf8");
function fn(name){const h="function "+name+"(";const i=src.indexOf(h);
 if(i<0)throw new Error("no "+name);
 let d=0,k=src.indexOf("{",i),instr=false,q="",esc=false,lc=false;
 for(;k<src.length;k++){const c=src[k];
  if(lc){if(c=="\n")lc=false;continue;}
  if(instr){if(esc)esc=false;else if(c=="\\")esc=true;else if(c==q)instr=false;continue;}
  if(c=='"'||c=="'"||c=="`"){instr=true;q=c;continue;}
  if(c=="/"&&src[k+1]=="*"){k=src.indexOf("*/",k)+1;continue;}
  if(c=="/"&&src[k+1]=="/"){lc=true;continue;}
  if(c=="{")d++;else if(c=="}"){d--;if(d==0)return src.slice(i,k+1);}}
 throw new Error("unbalanced "+name);}
function decl(name){const h="const "+name+"=";const i=src.indexOf(h);
 if(i<0)throw new Error("no "+name);
 let k=i+h.length;while(src[k]!="{"&&src[k]!="[")k++;
 let d=0,instr=false,q="",esc=false;
 for(;k<src.length;k++){const c=src[k];
  if(instr){if(esc)esc=false;else if(c=="\\")esc=true;else if(c==q)instr=false;continue;}
  if(c=='"'||c=="'"||c=="`"){instr=true;q=c;continue;}
  if(c=="{"||c=="[")d++;else if(c=="}"||c=="]"){d--;if(d==0)return src.slice(i,k+1);}}
 throw new Error("unbalanced "+name);}

const parts=["const DAY=86400000",
 "const addDays=(d,n)=>new Date(d.getTime()+n*DAY)",
 "var lang='en'", "var BIBLE_I18N={}",
 "var BIBLE=JSON.parse(fs.readFileSync(BIBLE_PATH,'utf8'))"];
for(const n of ["REF_BOOKS","WFIX","WOFF","WADV","PASCHAL_READINGS","DAILY_LIT",
                "AFTER_PENT_EP","MATT_GO","LUKE_SUN","LUKE_TAIL"]){
  try{parts.push(decl(n));}catch(e){}
}
// REF_BOOKS is extended by an Object.assign line for the Western books
for(const line of src.split("\n")) if(line.startsWith("Object.assign(REF_BOOKS,")) parts.push(line);
for(const n of ["juliOffset","pascha","fixedCivil","offsetFromPascha","adventSunday",
                "ordinal","westSlot","westReadingFor","refBook","parseRef","pericope"]){
  try{parts.push(fn(n));}catch(e){}
}
parts.push("globalThis.__sundayTables={AFTER_PENT_EP:AFTER_PENT_EP,MATT_GO:MATT_GO,LUKE_SUN:LUKE_SUN,LUKE_TAIL:LUKE_TAIL,PASCHAL_READINGS:PASCHAL_READINGS,DAILY_LIT:DAILY_LIT}");
eval(parts.join(";\n"));

const refs=new Map();
function note(ref,where){if(!ref)return;if(!refs.has(ref))refs.set(ref,where);}
for(let y=2025;y<=2029;y++){
  for(let i=0;i<400;i++){
    const d=new Date(y,0,1+i); if(d.getFullYear()!==y) break;
    let r=null; try{r=westReadingFor(d);}catch(e){}
    if(r){note(r.ep,"west");note(r.go,"west");}
  }
}

// The Sundays after Pentecost: the epistle series, the Matthaean gospels and
// the Sundays of Luke, which afterPentReading reads straight out of these.
// They are read from globalThis because a const declared inside eval() does
// not leak to the scope around it - the first attempt at this wrapped the
// lookup in a silent catch and reported the same 170 references as before,
// which is the whole reason the count is printed and compared.
const SUNDAY_TABLES = globalThis.__sundayTables || {};
// Reached through globalThis for the same reason as the Sunday tables: a
// const declared inside eval() does not leak to the scope around it, so
// naming these directly threw a ReferenceError that the catch swallowed.
// Both loops did nothing at all until this was noticed - the day Pascha's
// own readings were added and the count did not move.
for(const n of ["PASCHAL_READINGS","DAILY_LIT"]){
  if(!SUNDAY_TABLES[n]){console.error(n+" could not be reached; the check is not checking it");process.exit(2);}
}
for(const k in SUNDAY_TABLES.PASCHAL_READINGS){const r=SUNDAY_TABLES.PASCHAL_READINGS[k];if(r){note(r.ep,"paschal");note(r.go,"paschal");}}
for(const k in SUNDAY_TABLES.DAILY_LIT){const r=SUNDAY_TABLES.DAILY_LIT[k];if(r){note(r.e,"daily");note(r.g,"daily");}}
for(const n of ["AFTER_PENT_EP","MATT_GO","LUKE_SUN","LUKE_TAIL"]){
  const t = SUNDAY_TABLES[n];
  if(!t){ console.error("check_lectionary: " + n + " could not be reached"); process.exit(2); }
  for(const k in t){ const v=t[k]; if(typeof v==="string") note(v,"sundays"); }
}

const bad=[],empty=[];
for(const [ref,where] of refs){
  let p=null; try{p=parseRef(ref);}catch(e){}
  if(!p){bad.push(where+"  "+ref+"  (does not parse)");continue;}
  if(!BIBLE[p.book]){bad.push(where+"  "+ref+"  (no book "+p.book+" in the file)");continue;}
  let n=0; try{n=pericope(p.book,p.ranges).length;}catch(e){}
  if(!n) empty.push(where+"  "+ref+"  ("+p.book+" is there, the passage is not)");
}
console.log(JSON.stringify({total:refs.size,bad:bad,empty:empty}));
"""


def main():
    js = ("const PAGE=%s;const BIBLE_PATH=%s;\n"
          % (json.dumps(PAGE), json.dumps(BIBLE))) + HARNESS
    io.open("/tmp/lectcheck.js", "w", encoding="utf-8").write(js)
    out = subprocess.check_output(["node", "/tmp/lectcheck.js"]).decode("utf-8")
    d = json.loads(out.strip().splitlines()[-1])
    print("%d distinct references in the lectionaries" % d["total"])
    for line in d["empty"]:
        print("  review: %s" % line)
    for line in d["bad"]:
        print("  ERROR:  %s" % line)
    if d["bad"]:
        print("\n%d reference(s) the site cannot show." % len(d["bad"]))
        return 1
    print("every reference resolves to a book the site carries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
