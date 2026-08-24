# -*- coding: utf-8 -*-
"""The fasting rule the calendar prints.

What was here kept the four seasons and Wednesday and Friday, and stopped
there. It gave Great Saturday wine and oil, which is the one Saturday of the
year that has neither; it gave Palm Sunday wine where the Typikon gives fish;
it had no Exaltation of the Cross, no Beheading of the Forerunner and no eve
of Theophany, so three of the strictest days in the year showed as no fast at
all unless they happened to land on a Wednesday; and it gave every Church the
same Nativity and Apostles' fasts, which is the one place the local Churches
openly print different rules.

Sources, all published by the Churches themselves:

  Slavic and Antiochian usage, from the Typikon - Orthodox Church in America,
  "Fasting and Fast-Free Seasons of the Church", and the Antiochian
  Archdiocese's fasting rules: Monday, Wednesday and Friday without oil;
  Tuesday and Thursday wine and oil; Saturday and Sunday fish; and no fish
  from the twentieth of December whatever the day.

  Greek usage - Greek Orthodox Archdiocese of America: through the Nativity
  Fast fish, wine and oil on every day except Wednesday and Friday until the
  seventeenth of December, and the last week kept strictly.

  Council in Trullo, Canon 89, for the fast of Great Saturday; the Apostolic
  Canons 66 and 69 for the Wednesday and Friday obligation and its one
  exception.

    python3 tools/fasting_rule.py --write
"""
import io, re, sys

PATH = "index.html"
HEAD = "function fastingFor(d,mode){"

NEW = u'''function fastingFor(d,mode){
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
}'''


def replace_function(src, head, new):
    i = src.index(head)
    depth = 0
    j = i + len(head) - 1          # at the opening brace
    instr = False
    q = ""
    esc = False
    line_c = False
    k = j
    while k < len(src):
        c = src[k]
        if line_c:
            if c == "\n":
                line_c = False
            k += 1
            continue
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
        if c == "/" and src[k + 1:k + 2] == "*":
            k = src.index("*/", k) + 2
            continue
        if c == "/" and src[k + 1:k + 2] == "/":
            line_c = True
            k += 1
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return src[:i] + new + src[k + 1:]
        k += 1
    raise SystemExit("fastingFor: no closing brace")


def main():
    src = io.open(PATH, encoding="utf-8").read()
    if "Great and Holy Saturday - the fast is kept until midnight." in src:
        print("already installed")
        return
    out = replace_function(src, HEAD, NEW)
    if "--write" in sys.argv:
        io.open(PATH, "w", encoding="utf-8").write(out)
        print("wrote %s (%+d chars)" % (PATH, len(out) - len(src)))
    else:
        print("would rewrite fastingFor (%+d chars)" % (len(out) - len(src)))


if __name__ == "__main__":
    main()
