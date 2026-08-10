#!/usr/bin/env python3
"""
One masthead nav, the same on every page.

There were three. Five pages carried the design the site actually reads by -
12.5px, a maroon pill on the page you are standing on. The Library had its
own at 11px in grey with no pill, and the calendar a third at 11px with
vertical bars between the links and the current page merely coloured. The
same seven words looked like three different sites.

The five-page design wins, because it is the one most of the site already
wears and the only one that says plainly where the reader is. It is written
once here and installed on all seven pages, and the calendar's Guide and
About read exactly as the links do, so a page with more options is still the
same nav with more in it.

Scoped to .topnav rather than to bare `nav`, because the Library's catalog
and its section list are <nav> elements too and were being styled by rules
meant for the masthead.

The words are here too, and that is the harder half. The seven links looked
alike and said different things: the calendar translated all seven into
twenty-two languages, the Saints page into three, the Library and the Rule
into none at all, and the Contact page into nineteen for four of the links
and none for the other three. A reader in French met "Saints" on the
calendar and "Saints" on the Saints page for two different reasons, and a
reader in Georgian met his own language on one page and English on the next.
Four pages painted them from four private tables under three different
attribute names.

So the labels are written once, here, in every language the site offers, and
installed on all seven pages behind one attribute. No page keeps a nav word
of its own. Nothing was translated to do it: every one of the twenty-two
languages already had all seven words written somewhere on the site, and
they were gathered rather than composed. Where the pages disagreed, the
reading that most of them already showed the reader is the one kept.

    python3 tools/nav_chrome.py --check
    python3 tools/nav_chrome.py --write
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGES = ["index.html", "saints.html", "library.html", "prayers.html",
         "rule.html", "glossary.html", "contact.html"]

# ------------------------------------------------------------------ the words

# The order the links stand in, and where each one goes. A page links to
# itself with whatever href it already used, so that is left alone.
SLOTS = [("calendar", "/"), ("saints", "/saints"), ("library", "/library"),
         ("prayers", "/prayers"), ("rule", "/rule"),
         ("glossary", "/glossary"), ("contact", "/contact")]

# Gathered from what the pages already said, not composed here. Where they
# disagreed, the reading most of them showed is kept; the Greek Rule is the
# one exception, set monotonic because the Greek beside it is monotonic and a
# nav bar in two orthographies reads as a mistake.
NAV = {
    "en":  {"calendar": "Calendar", "saints": "Saints", "library": "Library", "prayers": "Prayers", "rule": "The Rule", "glossary": "Glossary", "contact": "Contact"},
    "el":  {"calendar": "Ημερολόγιο", "saints": "Άγιοι", "library": "Βιβλιοθήκη", "prayers": "Προσευχές", "rule": "Ο Κανόνας", "glossary": "Γλωσσάρι", "contact": "Επικοινωνία"},
    "ru":  {"calendar": "Календарь", "saints": "Святые", "library": "Библиотека", "prayers": "Молитвы", "rule": "Правило", "glossary": "Словарь", "contact": "Контакты"},
    "ro":  {"calendar": "Calendar", "saints": "Sfinți", "library": "Bibliotecă", "prayers": "Rugăciuni", "rule": "Pravila", "glossary": "Glosar", "contact": "Contact"},
    "uk":  {"calendar": "Календар", "saints": "Святі", "library": "Бібліотека", "prayers": "Молитви", "rule": "Правило", "glossary": "Словник", "contact": "Контакти"},
    "de":  {"calendar": "Kalender", "saints": "Heilige", "library": "Bibliothek", "prayers": "Gebete", "rule": "Die Regel", "glossary": "Glossar", "contact": "Kontakt"},
    "es":  {"calendar": "Calendario", "saints": "Santos", "library": "Biblioteca", "prayers": "Oraciones", "rule": "La Regla", "glossary": "Glosario", "contact": "Contacto"},
    "ar":  {"calendar": "التقويم", "saints": "القديسون", "library": "المكتبة", "prayers": "الصلوات", "rule": "القانون", "glossary": "مسرد", "contact": "اتصل بنا"},
    "fr":  {"calendar": "Calendrier", "saints": "Saints", "library": "Bibliothèque", "prayers": "Prières", "rule": "La Règle", "glossary": "Glossaire", "contact": "Contact"},
    "pt":  {"calendar": "Calendário", "saints": "Santos", "library": "Biblioteca", "prayers": "Orações", "rule": "A Regra", "glossary": "Glossário", "contact": "Contacto"},
    "it":  {"calendar": "Calendario", "saints": "Santi", "library": "Biblioteca", "prayers": "Preghiere", "rule": "La Regola", "glossary": "Glossario", "contact": "Contatti"},
    "sr":  {"calendar": "Календар", "saints": "Свети", "library": "Библиотека", "prayers": "Молитве", "rule": "Правило", "glossary": "Речник", "contact": "Контакт"},
    "ka":  {"calendar": "კალენდარი", "saints": "წმინდანები", "library": "ბიბლიოთეკა", "prayers": "ლოცვები", "rule": "წესი", "glossary": "ლექსიკონი", "contact": "კონტაქტი"},
    "zh":  {"calendar": "日历", "saints": "圣人", "library": "图书馆", "prayers": "祈祷文", "rule": "祈祷规则", "glossary": "词汇表", "contact": "联系"},
    "ja":  {"calendar": "暦", "saints": "聖人", "library": "図書室", "prayers": "祈祷文", "rule": "祈りの規矩", "glossary": "用語集", "contact": "お問い合わせ"},
    "ko":  {"calendar": "달력", "saints": "성인", "library": "도서관", "prayers": "기도문", "rule": "기도 규칙", "glossary": "용어집", "contact": "연락"},
    "sw":  {"calendar": "Kalenda", "saints": "Watakatifu", "library": "Maktaba", "prayers": "Sala", "rule": "Kanuni", "glossary": "Kamusi", "contact": "Mawasiliano"},
    "hy":  {"calendar": "Օրացույց", "saints": "Սուրբեր", "library": "Գրադարան", "prayers": "Աղոթքներ", "rule": "Կանոն", "glossary": "Բառարան", "contact": "Կապ"},
    "arc": {"calendar": "ܣܘܼܪܓܵܕܵܐ", "saints": "ܩܲܕܝܼܫܹ̈ܐ", "library": "ܒܹܝܬ ܐܲܪܟܹܐ", "prayers": "ܨܠܵܘܵܬܵܐ", "rule": "ܩܢܘܿܢܵܐ", "glossary": "ܡܸܠܘܵܐܐ", "contact": "ܩܘܼܢܵܛܵܐ"},
    "hi":  {"calendar": "पंचांग", "saints": "संत", "library": "पुस्तकालय", "prayers": "प्रार्थनाएँ", "rule": "नियम", "glossary": "शब्दावली", "contact": "संपर्क"},
    "bn":  {"calendar": "পঞ্জিকা", "saints": "সাধুগণ", "library": "গ্রন্থাগার", "prayers": "প্রার্থনা", "rule": "নিয়ম", "glossary": "শব্দকোষ", "contact": "যোগাযোগ"},
    "ur":  {"calendar": "تقویم", "saints": "مقدسین", "library": "کتب خانہ", "prayers": "دعائیں", "rule": "قاعدہ", "glossary": "لغت", "contact": "رابطہ"},
}


# The link the reader is standing on, per page, so the one that points at "#"
# can still be told which word it wants.
SELF = {"index.html": "calendar", "saints.html": "saints",
        "library.html": "library", "prayers.html": "prayers",
        "rule.html": "rule", "glossary.html": "glossary",
        "contact.html": "contact"}

# The one line each page runs when the reader picks a language. The nav is
# not the page's to repaint, so the page says only that the language changed.
# Anchored on the line that stores the choice, which every page has exactly
# one of, and which is the moment the choice becomes true.
SAYS = {
    "index.html":
        ('try{localStorage.setItem("plithos.lang",lang);}catch(e){}', "lang"),
    "saints.html":
        ('try{ localStorage.setItem("plithos.lang",L); }catch(e){}', "L"),
    "library.html":
        ('try{localStorage.setItem("plithos.lang",l);}catch(e){} applyChrome();', "l"),
    "prayers.html":
        ('try{ localStorage.setItem("plithos.lang",lang); }catch(e){}', "lang"),
    "rule.html":
        ('try{ localStorage.setItem(KEY,L); }catch(e){}', "L"),
    "glossary.html":
        ('try{ localStorage.setItem("plithos.lang",L); }catch(e){}', "L"),
    "contact.html":
        ('try{ localStorage.setItem("plithos.lang",sel.value); }catch(e){}', "sel.value"),
}

TELL = 'document.dispatchEvent(new CustomEvent("plithos:lang",{detail:%s}));'

# Named without naming this file: nothing in a served page describes how the
# page was made. tools/check_site.py enforces that and caught it.
MARK = "/* The masthead nav, one design on every page. */"
JSMARK = "/* The masthead nav says the same seven words on every page. */"

# Held inline rather than fetched: it is the first thing a reader sees, it is
# four kilobytes, and a nav that arrives a moment after the page and changes
# under his eye is worse than one that is simply there. English stands in the
# markup, so a browser that runs no script at all still reads a whole nav.
NAVJS = JSMARK + """
(function(){
  var NAV=%s;
  function paint(L){
    var t=NAV[L]||NAV.en,a=document.querySelectorAll(".topnav [data-nav]"),i,v;
    for(i=0;i<a.length;i++){
      v=t[a[i].getAttribute("data-nav")];
      if(v)a[i].textContent=v;
    }
  }
  function chosen(){
    var L=null;
    try{ L=localStorage.getItem("plithos.lang"); }catch(e){}
    return (L&&NAV[L])?L:"en";
  }
  paint(chosen());
  document.addEventListener("plithos:lang",function(e){
    paint((e&&e.detail&&NAV[e.detail])?e.detail:chosen());
  });
})();"""

# The dark theme is not repeated here: assets/plithos-ui.*.css already turns
# the pill on `nav a[aria-current=page]` to the deep red and keeps the links
# free of the underline it gives every other link.
CSS = MARK + """
.topnav{display:flex;flex-wrap:wrap;align-items:center;gap:2px;min-width:0;flex-shrink:1}
.topnav a,.topnav button{font-family:var(--mono);font-size:12.5px;font-weight:400;line-height:1.2;
  text-transform:uppercase;letter-spacing:.06em;color:var(--ink-soft);white-space:nowrap;
  padding:7px 11px;border-radius:7px;background:none;border:0;margin:0;cursor:pointer;
  text-decoration:none}
.topnav a:hover,.topnav button:hover{background:var(--rail);color:var(--ink)}
.topnav a:focus-visible,.topnav button:focus-visible{outline:2px solid var(--porphyry);outline-offset:2px}
.topnav a[aria-current=page]{background:var(--porphyry);color:#f2ece0}
"""

# Every rule any page used to style the masthead nav with. Removed wholesale
# so the block above is the only thing that speaks.
DEAD = re.compile(
    r"^(?:nav\{|nav a\b|nav a:hover|\.nav\{|\.nav>|\.nav a\b|\.navbtn|\.topnav)"
    r"[^\n]*\n", re.M)

# A rule can run onto a second line; these are the ones that do.
DEAD_MULTI = [
    ".nav{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);display:flex;flex-wrap:nowrap;flex-shrink:0;gap:0;align-items:center}\n",
]

# The comment that explained a rule now gone.
DEAD_COMMENT = """/* Seven links and the two controls the shared layer mounts beside them do not
   fit a phone on one line, and a 1fr track will not go below its content, so
   the month grid pushed the page wider than the screen. Let both give way. */
"""


def masthead_nav(s):
    """(start, end) of the opening <nav> tag that holds the site links."""
    for m in re.finditer(r"<nav\b[^>]*>", s):
        after = s[m.end():m.end() + 400]
        # The page you are on links to itself with "#", so no single href is
        # present on all seven. Two of the others always are.
        hrefs = sum(1 for h in ('/saints', '/library', '/prayers', '/rule',
                                '/glossary', '/contact')
                    if ('href="%s"' % h) in after)
        if hrefs >= 4:
            return m.start(), m.end()
    return None


def nav_block(s, open_span):
    """(start, end) of the whole masthead nav, opening tag to </nav>."""
    a, b = open_span
    end = s.index("</nav>", b) + len("</nav>")
    return a, end


def label_links(name, block):
    """One attribute on every link, the English word inside it, and no page's
    private key left on any of them.

    The href says which of the seven a link is, except for the one the page
    points at itself, which several pages write as "#"."""
    slot_of = dict((href, slot) for slot, href in SLOTS)
    changed = [0]

    def one(m):
        tag, text = m.group(1), m.group(2)
        href = re.search(r'href="([^"]*)"', tag)
        if not href:
            return m.group(0)
        slot = slot_of.get(href.group(1))
        if slot is None:
            slot = SELF[name] if 'aria-current="page"' in tag else None
        if slot is None:
            return m.group(0)
        new = re.sub(r'\s+data-(?:i18n|ui|t|nav)="[^"]*"', "", tag)
        new = new[:-1].rstrip() + ' data-nav="%s">' % slot
        word = NAV["en"][slot]
        if new + word != tag + text:
            changed[0] += 1
        return new + word + "</a>"

    return re.sub(r"(<a\b[^>]*>)([^<]*)</a>", one, block), changed[0]


def fix(name, s):
    notes = []

    # 1. the nav carries the class the rules are written against
    span = masthead_nav(s)
    if not span:
        notes.append("no masthead nav found")
        return s, notes
    a, b = span
    tag = s[a:b]
    new = re.sub(r'\s*class="[^"]*"', "", tag)
    new = new[:4] + ' class="topnav"' + new[4:]
    if new != tag:
        notes.append("nav class -> topnav")
        s = s[:a] + new + s[b:]

    # 2. the old rules go
    head_end = s.index("</style>")
    head, tail = s[:head_end], s[head_end:]
    for d in DEAD_MULTI:
        if d in head:
            head = head.replace(d, "")
            notes.append("removed a wrapped rule")
    if DEAD_COMMENT in head:
        head = head.replace(DEAD_COMMENT, "")
        notes.append("removed a stale note")
    head, n = DEAD.subn("", head)
    if n:
        notes.append("removed %d rules" % n)

    # 3. and the one block goes in last, so nothing left can outrank it
    head = re.sub(re.escape(MARK) + r".*?\n(?=\S|\Z)", "", head, flags=re.S)
    head = head.rstrip("\n") + "\n" + CSS
    s = head + tail

    # 4. every link says which of the seven it is, and nothing else
    a, b = nav_block(s, masthead_nav(s))
    block, n = label_links(name, s[a:b])
    if n:
        notes.append("%d link(s) relabelled" % n)
    s = s[:a] + block + s[b:]

    # 5. the words, and the one line that repaints them
    table = json.dumps({k: NAV[k] for k in NAV}, ensure_ascii=False,
                       separators=(",", ":"), sort_keys=True)
    script = "<script>" + (NAVJS % table) + "\n</script>"
    s = re.sub(r"<script>" + re.escape(JSMARK) + r".*?</script>\s*", "",
               s, flags=re.S)
    end = s.index("</nav>", a) + len("</nav>")
    if s[end:end + 1] != "\n":
        script = "\n" + script
    s = s[:end] + script + s[end:]
    notes.append("words installed")

    anchor, var = SAYS[name]
    tell = TELL % var
    if tell not in s:
        if anchor not in s:
            notes.append("NO ANCHOR for the language line")
        elif s.count(anchor) != 1:
            notes.append("the language line is not unique")
        else:
            s = s.replace(anchor, anchor + tell, 1)
            notes.append("says when the language changes")
    return s, notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if not (a.write or a.check):
        a.check = True

    for name in PAGES:
        p = ROOT / name
        s = p.read_text(encoding="utf-8")
        out, notes = fix(name, s)
        print("%-14s %s" % (name, "; ".join(notes) or "already uniform"))
        if a.write and out != s:
            p.write_text(out, encoding="utf-8")
    if a.write:
        print("written")
    else:
        print("(--check: nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
