/* The calendar's reckoning, copied out of index.html by
 * tools/build_calendar_engine.py. DO NOT EDIT. Edit the calendar and run the
 * tool; check_site.py fails if the two disagree.
 *
 * The functions below are the page's own, unchanged. They read lang, mode,
 * rite, juris and saintsScope as free variables; here those are bindings in
 * this closure, so the same code means the same thing it means in the page.
 */
export function calendar(TABLES, NAMES, NAMES_LANG){
  const {LUKE_SUN, LUKE_BEFORE_FF, WEPI, WXMAS, WPENT, MATT_GO, I18N, FASTNOTE_I18N, FAST, JURISDICTIONS, TWELVE_FIXED, TWELVE_MOVABLE, MAJOR_FIXED, PASCHAL_NAMES, PASCHAL_READINGS, DAILY_LIT, SYNAXARION, MOVABLE_SYNAXARION, LOCAL_FIXED, LOCAL_MOVABLE, LOCAL_CIVIL, OMIT_FIXED, AFTER_PENT_EP, WFIX, WOFF, WADV, WESTERN_FIXED, WESTERN_MOVABLE} = TABLES;
  /* One language's names, as the page's own table is shaped. tn() is the
     page's function, unchanged, and reads NAMES_I18N[name][lang]. */
  const NAMES_I18N = {};
  if (NAMES) { const L = NAMES_LANG || "en";
    for (const k in NAMES) { const o = {}; o[L] = NAMES[k]; NAMES_I18N[k] = o; } }

  let lang="en", mode="new", rite="byzantine", juris="greek",
      saintsScope="church", saintsPick=new Set(Object.keys(TABLES.JURISDICTIONS));

  const SUN_AP={en:n=>ordinal(n)+" Sunday after Pentecost",el:n=>n+"η Κυριακή μετά την Πεντηκοστή",ru:n=>n+"-я Неделя по Пятидесятнице",ro:n=>"Duminica a "+n+"-a după Rusalii",uk:n=>n+"-та Неділя після П’ятидесятниці",de:n=>n+". Sonntag nach Pfingsten",es:n=>"Domingo "+n+"º después de Pentecostés",ar:n=>"الأحد "+n+" بعد العنصرة"};
  const DAY=86400000;
  const MN=["January","February","March","April","May","June","July","August","September","October","November","December"];
  const addDays=(d,n)=>new Date(d.getTime()+n*DAY);
  const fmtISO=d=>d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");
  const pad=n=>String(n).padStart(2,"0");
  const T=()=>I18N[lang]||I18N.en;
  const Lmon=m=>T().months[m], Lday=w=>T().days[w], Lshort=w=>T().short[w], fastLabel=k=>(T().fast[k]||I18N.en.fast[k]);
  const t=k=>T().ui[k]||I18N.en.ui[k]||k;
  function westGreenSunday(d,y,off,adv1){
  const P=Math.round((off-49)/7);                 // Roman position (Trinity=1 at off 56)
  const lastSun=addDays(adv1,-7);
  const T=Math.round((offsetFromPascha(lastSun,pascha(y))-49)/7);
  if(P===T) return WPENT[24];                      // Last Sunday always uses the 24th propers
  if(P<=23) return WPENT[P];
  const K=T-1-23, epiN=6-K+(P-23);                 // resumed Sundays after Epiphany, ascending
  return WEPI[epiN]||WPENT[24];
}
  function sundayAP(n){return (SUN_AP[lang]||SUN_AP.en)(n);}
  function juliOffset(y){return Math.floor(y/100)-Math.floor(y/400)-2;}
  function pascha(y){                                                              // Gregorian civil date of Orthodox Pascha
  const a=y%4,b=y%7,c=y%19,d=(19*c+15)%30,e=(2*a+4*b-d+34)%7;
  const month=Math.floor((d+e+114)/31),day=((d+e+114)%31)+1;
  return addDays(new Date(y,month-1,day),juliOffset(y));
}
  function fixedCivil(mo,da,y,mode){const base=new Date(y,mo-1,da);return mode==="old"?addDays(base,juliOffset(y)):base;}
  function nthWeekday(y,mo,dow,n){let c=0;for(let d=1;d<=31;d++){const dt=new Date(y,mo-1,d);if(dt.getMonth()!==mo-1)break;if(dt.getDay()===dow){c++;if(c===n)return dt;}}return null;}
  function lastWeekday(y,mo,dow){let r=null;for(let d=1;d<=31;d++){const dt=new Date(y,mo-1,d);if(dt.getMonth()!==mo-1)break;if(dt.getDay()===dow)r=dt;}return r;}
  function adventSunday(y){const xmas=fixedCivil(12,25,y,"new");let s=addDays(xmas,-1);while(s.getDay()!==0)s=addDays(s,-1);return addDays(s,-21);}
  function ordinal(n){const s=["th","st","nd","rd"],v=n%100;return n+(s[(v-20)%10]||s[v]||s[0]);}
  function offsetFromPascha(d,p){return Math.round((new Date(d.getFullYear(),d.getMonth(),d.getDate())-new Date(p.getFullYear(),p.getMonth(),p.getDate()))/DAY);}
  function prevSun(x){return addDays(x,-(x.getDay()||7));}
  function nextSun(x){return addDays(x,(7-x.getDay())||7);}
  function westSlot(d){
  const y=d.getFullYear(), p=pascha(y), off=offsetFromPascha(d,p), dow=d.getDay();
  const mmdd=String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");
  if(WFIX[mmdd]) return WFIX[mmdd];                 // great fixed feast overrides
  if(WOFF[off]) return WOFF[off];                   // Easter-anchored proper-offset day
  if(dow===0){
    const adv1=adventSunday(y), xmas=fixedCivil(12,25,y,"new"), epi=fixedCivil(1,6,y,"new");
    if(off>56 && d<adv1) return westGreenSunday(d,y,off,adv1);
    if(d>=adv1 && d<xmas){const n=Math.round((d-adv1)/(7*DAY))+1; if(WADV[n])return WADV[n];}
    if(d>epi && off<-63){const n=Math.round((d-epi)/(7*DAY)); if(n>=1&&WEPI[n])return WEPI[n];}
    return WXMAS.sunAfterXmas;
  }
  let s=addDays(d,-1); while(s.getDay()!==0) s=addDays(s,-1);   // ferial: repeat preceding Sunday
  return westSlot(s);
}
  function westReadingFor(d){const r=westSlot(d);return r?{ep:r.e,go:r.g}:null;}
  function commemsWestern(d){
  const y=d.getFullYear(),out=[],p=pascha(y),off=offsetFromPascha(d,p),key=String(off);
  for(const f of WESTERN_FIXED){const c=fixedCivil(f.mo,f.da,y,"new");if(c.getMonth()===d.getMonth()&&c.getDate()===d.getDate())out.push({...f,cal:""});}
  const ember={"-39":1,"-37":1,"-36":1,"52":1,"54":1,"55":1}, rogation={"36":1,"37":1,"38":1};
  if(ember[key])out.push({name:"Ember Day",strict:true,cal:""});
  if(rogation[key])out.push({name:"Rogation Day",cal:""});
  let dayName=WESTERN_MOVABLE[key]||null;
  if(!dayName&&d.getDay()===0){
    const adv1=adventSunday(y),xmas=fixedCivil(12,25,y,"new"),epi=fixedCivil(1,6,y,"new");
    if(d>=adv1&&d<xmas)dayName=ordinal(Math.round((d-adv1)/(7*DAY))+1)+" Sunday in Advent";
    else if(off>56&&d<adv1){const P=Math.round((off-49)/7),lastSun=addDays(adv1,-7),T=Math.round((offsetFromPascha(lastSun,pascha(y))-49)/7);
      if(P===T)dayName="Last Sunday after Pentecost";
      else if(P<=23)dayName=ordinal(P)+" Sunday after Pentecost";
      else{const K=T-1-23,epiN=6-K+(P-23);dayName=ordinal(epiN)+" Sunday after Epiphany (resumed)";}}
    else if(d>epi&&off< -63){const n=Math.round((d-epi)/(7*DAY));if(n>=1)dayName=ordinal(n)+" Sunday after Epiphany";}
  }
  if(!dayName){const xmas=fixedCivil(12,25,y,"new"),epi=fixedCivil(1,6,y,"new");if(d>=xmas||d<epi)dayName="Christmastide";}
  return {commems:out,dayName,dayReading:westReadingFor(d)};
}
  function fastingWestern(d){
  const y=d.getFullYear(),p=pascha(y),off=offsetFromPascha(d,p),dow=d.getDay();
  const within=(a,b)=>off>=a&&off<=b;let fast=null,note="";
  if(within(0,6)){fast="free";note="Easter Week — the Octave of Easter.";}
  else if(within(-46,-1)){fast=(dow===0||dow===6)?"wine":"strict";note=within(-6,-1)?"Holy Week.":"Lent (from Ash Wednesday). The Shrovetide Sundays before it are not fasting days.";}
  if(!fast){const adv1=adventSunday(y),xmas=fixedCivil(12,25,y,"new");if(d>=adv1&&d<xmas){fast=(dow===0||dow===6)?"fish":"wine";note="Advent — a season of fasting and preparation.";}}
  const inSeason=(sm,sd,em,ed)=>{const s=fixedCivil(sm,sd,y,"new"),e=fixedCivil(em,ed,y,"new");return d>=s&&d<=e;};
  if(!fast&&inSeason(8,1,8,14)){fast=(dow===0||dow===6)?"wine":"strict";note="The Dormition Fast.";}
  const apStart=addDays(p,57),apEnd=addDays(fixedCivil(6,29,y,"new"),-1);
  if(!fast&&d>=apStart&&d<=apEnd){fast=(dow===2||dow===4||dow===0||dow===6)?"fish":"wine";note="The Apostles' Fast.";}
  if(!fast&&(dow===3||dow===5)){fast="strict";note="Wednesday and Friday are kept with abstinence.";}
  if(!fast)fast="none";return {info:FAST[fast],note};
}
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
  function afterPentReading(d,N){
  const y=d.getFullYear(), mo=d.getMonth(), sm=(a,b)=>a.getMonth()===b.getMonth()&&a.getDate()===b.getDate();
  const yE = mo<=2 ? y-1 : y;   /* Elevation/Nativity belong to the prior year for Jan-Mar dates */
  const yT = mo>=6 ? y+1 : y;   /* Theophany belongs to the next year for Jul-Dec dates */
  const E=fixedCivil(9,14,yE,mode), sbE=prevSun(E), saE=nextSun(E);
  const NV=fixedCivil(12,25,yE,mode), sbN=prevSun(NV), saN=nextSun(NV), ff=addDays(sbN,-7);
  const TH=fixedCivil(1,6,yT,mode), sbT=prevSun(TH), saT=nextSun(TH);
  if(sm(d,sbE))return {ep:"Gal. 6:11-18",go:"John 3:13-17",name:"Sunday before the Elevation of the Cross"};
  if(sm(d,saE))return {ep:"Gal. 2:16-20",go:"Mark 8:34-9:1",name:"Sunday after the Elevation of the Cross"};
  if(sm(d,ff)) return {ep:"Col. 3:4-11",go:"Luke 14:16-24",name:"Sunday of the Holy Forefathers"};
  if(sm(d,sbN))return {ep:"Heb. 11:9-10, 32-40",go:"Matt. 1:1-25",name:"Sunday before the Nativity"};
  if(sm(d,saN))return {ep:"Gal. 1:11-19",go:"Matt. 2:13-23",name:"Sunday after the Nativity"};
  if(sm(d,sbT))return {ep:"2 Tim. 4:5-8",go:"Mark 1:1-8",name:"Sunday before the Theophany"};
  if(sm(d,saT))return {ep:"Eph. 4:7-13",go:"Matt. 4:12-17",name:"Sunday after the Theophany"};
  const ep=AFTER_PENT_EP[Math.min(N,32)]||null;
  if(d<saE)return {ep,go:MATT_GO[Math.min(N,17)]||null};
  const L=Math.round((d-saE)/(7*DAY));
  if(L>=1&&L<=LUKE_SUN.length)return {ep,go:LUKE_SUN[L-1]};const back=Math.round((ff-d)/(7*DAY));if(back>=1&&back<=LUKE_BEFORE_FF.length)return {ep,go:LUKE_BEFORE_FF[back-1]};
  return {ep,go:null,prov:true};
}
  function commemsFor(d,mode){
  if(rite==="western")return commemsWestern(d);
  const y=d.getFullYear(), out=[]; let principal=false;
  for(const f of TWELVE_FIXED){const c=fixedCivil(f.mo,f.da,y,mode);if(c.getMonth()===d.getMonth()&&c.getDate()===d.getDate()){out.push({...f,great:true,cal:""});principal=true;}}
  for(const f of MAJOR_FIXED){const c=fixedCivil(f.mo,f.da,y,mode);if(c.getMonth()===d.getMonth()&&c.getDate()===d.getDate()){out.push({...f,great:false,cal:""});principal=true;}}
  {const men=mode==="old"?addDays(d,-juliOffset(y)):d;const mk=pad(men.getMonth()+1)+"-"+pad(men.getDate());const syn=SYNAXARION[mk];if(syn)for(const s of syn){if(principal&&s.g)continue;if(out.some(o=>o.name===s.n))continue;out.push({name:s.n,great:!!s.g,cal:"",mmdd:mk});}}
  /* What this Church does not keep. The calendar's base is one synaxarion and
   every jurisdiction was only ever able to ADD to it, so a Greek reader was
   shown North American commemorations his Church does not keep. A jurisdiction
   declines a base entry by naming it here; nothing is declined without a
   source, because telling a reader his Church does not keep a feast that she
   does is worse than the fault it mends. */
{const _sk=scopeKeys();const decl=(_sk.length===1)?(OMIT_FIXED[_sk[0]]||null):null;
 if(decl&&decl.length){for(let oi=out.length-1;oi>=0;oi--){const nm=out[oi].name||"";
   if(out[oi].local)continue;
   if(decl.some(function(x){return nm.indexOf(x.name)>=0;}))out.splice(oi,1);}}}
/* A Church renames a base commemoration for itself - Vladimir into
     Volodymyr - and that only makes sense while one Church is in scope. */
  const isAll = scopeKeys().length!==1;
  const locals = dedupeLocal();
  for(const f of locals){const c=fixedCivil(f.mo,f.da,y,mode);if(c.getMonth()!==d.getMonth()||c.getDate()!==d.getDate())continue;if(f.base){if(isAll)continue;const bi=out.findIndex(o=>!o.local&&o.name&&new RegExp("\\b"+f.base+"\\b","i").test(o.name));if(bi>=0){out[bi]={...out[bi],name:f.name,local:true,j:f.j};}else{out.push({...f,great:false,local:true,cal:""});}}else{out.push({...f,great:false,local:true,cal:""});}}
  const p=pascha(y), off=offsetFromPascha(d,p), key=String(off);
  if(TWELVE_MOVABLE[key])out.unshift({...TWELVE_MOVABLE[key],great:true,cal:""});
  const lmovs = dedupeLocalMovable();
  for(const m of lmovs){ if(m.off===off) out.push({name:m.name,great:false,local:true,j:m.j,cal:""}); }
  const lcivs = dedupeLocalCivil();
  for(const m of lcivs){ if(d.getMonth()===m.mo-1 && d.getDay()===m.dow && Math.ceil(d.getDate()/7)===m.nth) out.push({name:m.name,great:false,local:true,j:m.j,cal:""}); }
  let dayName=null, dayReading=null, movKey=null;
  if(PASCHAL_READINGS[key])dayReading=PASCHAL_READINGS[key];if(PASCHAL_NAMES[key]){dayName=tn(PASCHAL_NAMES[key]);}
  else if(d.getDay()===0){
    let N=null;
    if(off>56) N=Math.round((off-49)/7);
    else if(off<-77 && off>-160){const op=offsetFromPascha(d,pascha(d.getFullYear()-1)); if(op>56) N=Math.round((op-49)/7);}
    if(N!==null){const r=afterPentReading(d,N);dayReading=r;dayName=r.name?tn(r.name):sundayAP(N);movKey=r.name||null;}
  }
  else {
    const mcday = off < -70 ? offsetFromPascha(d,pascha(d.getFullYear()-1))+71 : off+71;
    const L=DAILY_LIT[mcday];
    if(L) dayReading = L.g ? {ep:L.e,go:L.g} : {ep:L.e,prov:true};
    else if(off>=-53 && off<=-2) dayReading={aliturgical:true};
  }
  if(dayReading===null && d.getDay()>=1 && d.getDay()<=5 && off>=-53 && off<=-1) dayReading={aliturgical:true};
  if(movKey&&MOVABLE_SYNAXARION[movKey]){for(const ms of MOVABLE_SYNAXARION[movKey]){if(!out.some(o=>o.name===ms.n))out.push({name:ms.n,great:!!ms.g,movable:true});}}
  return {commems:out,dayName,dayReading};
}
  function fastingFor(d,mode){
  const m=mode==="both"?"new":mode, y=d.getFullYear(), p=pascha(y), off=offsetFromPascha(d,p), dow=d.getDay();
  const within=(a,b)=>off>=a&&off<=b;
  const on=(mo,da)=>{const c=fixedCivil(mo,da,y,m);return c.getMonth()===d.getMonth()&&c.getDate()===d.getDate();};
  /* The Nativity and the Apostles' fasts are where the Churches print
     different rules rather than the same rule kept differently. Constantinople
     and the Church of Greece give fish on every day but Wednesday and Friday;
     the Typikon, which the Slavic Churches and Antioch publish, keeps fish to
     Saturday and Sunday and leaves Monday, Wednesday and Friday without oil.
     Both are published; neither is the other's relaxation. */
  const greek=(typeof juris!=="undefined"&&juris==="greek");
  let fast=null, note="";
  if(within(0,6)){fast="free";note="Pascha and Bright Week.";}
  else if(within(50,55)){fast="free";note="The week after Pentecost.";}
  else if(within(-69,-64)){fast="free";note="The week after the Publican and the Pharisee.";}
  if(!fast){
    const half=d.getMonth()>=6, natC=fixedCivil(12,25,half?y:y-1,m), theoC=fixedCivil(1,6,half?y+1:y,m);
    if(d>=natC&&d<=addDays(theoC,-2)){fast="free";note="The festal days from the Nativity to the eve of Theophany.";}
  }
  if(!fast&&within(-55,-49)){fast="dairy";note="Cheesefare week - no meat; dairy, eggs and fish are permitted all week.";}
  if(!fast&&within(-48,-1)){
    /* Great Saturday is the single Saturday of the year kept without wine or
       oil, and the fast runs to midnight (Trullo 89). The Annunciation and
       Palm Sunday carry fish through Lent; Lazarus Saturday, wine and oil. */
    if(off===-1){fast="strict";note="Great and Holy Saturday - the fast is kept until midnight.";}
    else if(off===-7){fast="fish";note="Palm Sunday - fish is given.";}
    else if(off===-8){fast="wine";note="Lazarus Saturday - wine and oil are given.";}
    else if(on(3,25)){fast="fish";note="The Annunciation - fish is given even in Lent.";}
    else if(dow===0||dow===6){fast="wine";note=within(-6,-1)?"Great and Holy Week - the strictest days of the year.":"Great Lent - wine and oil on Saturdays and Sundays.";}
    else {fast="strict";note=within(-6,-1)?"Great and Holy Week - the strictest days of the year.":"Great Lent.";}
  }
  const inSeason=(sm,sd,em,ed)=>{const s=fixedCivil(sm,sd,y,m),e=fixedCivil(em,ed,y,m);return d>=s&&d<=e;};
  if(!fast&&inSeason(11,15,12,24)){
    if(on(11,21)){fast="fish";note="The Entry of the Theotokos into the Temple - fish is given.";}
    else if(greek){
      if(d>=fixedCivil(12,18,y,m)){fast=(dow===3||dow===5)?"strict":((dow===0||dow===6)?"wine":"strict");note="The Nativity Fast. The last days before the feast are kept strictly.";}
      else{fast=(dow===3||dow===5)?"strict":"fish";note="The Nativity Fast. In Greek usage fish is given on every day but Wednesday and Friday until Dec 17.";}
    }
    else if(d>=fixedCivil(12,20,y,m)){fast=(dow===0||dow===6)?"wine":"strict";note="The Nativity Fast. From Dec 20 no fish is given, whatever the day.";}
    else{fast=(dow===0||dow===6)?"fish":((dow===2||dow===4)?"wine":"strict");note="The Nativity Fast. Fish on Saturdays and Sundays; wine and oil on Tuesdays and Thursdays.";}
  }
  if(!fast&&inSeason(8,1,8,14)){
    if(on(8,6)){fast="fish";note="The Transfiguration - the one day of the Dormition Fast on which fish is given.";}
    else{fast=(dow===0||dow===6)?"wine":"strict";note="The Dormition Fast, among the strictest of the year.";}
  }
  const apStart=addDays(p,57),apEnd=addDays(fixedCivil(6,29,y,m),-1);
  if(!fast&&d>=apStart&&d<=apEnd){
    if(greek){fast=(dow===3||dow===5)?"strict":"fish";note="The Apostles' Fast. In Greek usage fish is given on every day but Wednesday and Friday.";}
    else{fast=(dow===0||dow===6)?"fish":((dow===2||dow===4)?"wine":"strict");note="The Apostles' Fast. Fish on Saturdays and Sundays; wine and oil on Tuesdays and Thursdays.";}
  }
  /* Three days are kept strictly wherever in the week they fall. */
  if(!fast){
    if(on(9,14)){fast="strict";note="The Exaltation of the Cross is a strict fast on whatever day it falls.";}
    else if(on(8,29)){fast="strict";note="The Beheading of the Forerunner is a strict fast on whatever day it falls.";}
    else if(on(1,5)){fast="strict";note="The eve of Theophany is a strict fast.";}
  }
  if(!fast&&(dow===3||dow===5)){
    /* A Great Feast falling on a Wednesday or a Friday outside the seasons is
       kept with fish. The Exaltation is the exception and was taken above. */
    const gf=TWELVE_FIXED.some(function(f){return f.mo!==9||f.da!==14?on(f.mo,f.da):false;});
    if(gf){fast="fish";note="A Great Feast on a fast day - fish is given.";}
    else{fast="strict";note="Wednesday and Friday are kept as fast days through the year.";}
  }
  if(!fast)fast="none";
  return {info:FAST[fast],note};
}
  function tn(s){const e=NAMES_I18N[s];return (e&&(e[lang]||e.en))||s;}
  function fnote(s){if(!s)return s;const e=FASTNOTE_I18N[s];return (e&&(e[lang]||s))||s;}
  function dayData(d){
  const {commems,dayName,dayReading}=commemsFor(d,mode);
  let fast=rite==="western"?fastingWestern(d):fastingFor(d,mode);
  const strictFeast=commems.find(c=>c.strict);
  const relax=commems.find(c=>c.great||c.fish||c.free);
  if(strictFeast)fast={info:FAST.strict,note:"A day of strict fasting."};
  else if(relax&&(fast.info.k==="strict"||fast.info.k==="wine"))fast=relax.free?{info:FAST.free,note:"The fast is relaxed for the feast."}:{info:FAST.fish,note:"Fish is permitted for the feast."};
  const headline=commems.length?tn(commems[0].name):(dayName||Lday(d.getDay()));
  const great=commems.some(c=>c.great)||/PASCHA/.test(headline);
  return {commems,dayName,fast,headline,great,dayReading:dayReading||null};
}
  /* The one thing written here rather than copied: the way in. */

  /* A word in the reader's language, English where his has none. The tables
     already carry every one of these; an earlier draft of this file simply
     did not ask for them, and answered an Arabic reader in English. */
  function say(group, key){
    const mine = TABLES.I18N[lang] && TABLES.I18N[lang][group];
    return (mine && mine[key]) || TABLES.I18N.en[group][key] || key;
  }

  /* A Church is named, not keyed. "greek" is how the calendar files it. */
  function churchName(k){
    const u = TABLES.I18N[lang] && TABLES.I18N[lang].ui;
    if (u && u["jz_" + k]) return u["jz_" + k];
    const e = TABLES.I18N.en.ui;
    if (e && e["jz_" + k]) return e["jz_" + k];
    return (TABLES.JURISDICTIONS[k] || {}).name || k;
  }

  return function day(iso, opts){
    opts = opts || {};
    const j = TABLES.JURISDICTIONS[opts.juris] ? opts.juris : "greek";
    juris = j;
    rite = TABLES.JURISDICTIONS[j].rite;
    mode = (opts.cal === "old" || opts.cal === "new") ? opts.cal
                                                      : TABLES.JURISDICTIONS[j].cal;
    lang = TABLES.I18N[opts.lang] ? opts.lang : "en";
    saintsScope = (opts.scope === "all") ? "all" : "church";
    const p = String(iso).split("-").map(Number);
    const d = new Date(p[0], p[1] - 1, p[2]);
    if (isNaN(d.getTime())) return null;
    const dd = dayData(d);
    const os = addDays(d, -juliOffset(d.getFullYear()));
    return {
      date: fmtISO(d),
      julian: fmtISO(os),
      jurisdiction: j,
      jurisdiction_name: churchName(j),
      calendar: mode,
      rite: rite,
      language: lang,
      day_name: dd.dayName || null,
      headline: dd.headline,
      great: !!dd.great,
      commemorations: dd.commems.map(function(c){
        return { name: tn(c.name), english: c.name, great: !!c.great,
                 local: !!c.local, church: c.j || null,
                 church_name: c.j ? churchName(c.j) : null };
      }),
      fast: { level: dd.fast.info.k, label: say("fast", dd.fast.info.k),
              english: dd.fast.info.label,
              note: dd.fast.note ? fnote(dd.fast.note) : "" },
      readings: dd.dayReading
        ? { epistle: dd.dayReading.ep || null, gospel: dd.dayReading.go || null,
            epistle_label: say("ui", "epistle"), gospel_label: say("ui", "gospel") }
        : null
    };
  };
}
