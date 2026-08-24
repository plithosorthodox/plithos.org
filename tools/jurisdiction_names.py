# -*- coding: utf-8 -*-
"""The Georgian and the Bulgarian Churches, named in every language.

The jurisdiction picker asks for jz_georgian and jz_bulgarian, and until now
no language answered: the two Churches were added after the picker's words
were written, so a Russian reader chose between eight Churches in Russian and
two in English. The names follow the form the neighbouring entries take -
the adjective agreeing with "Church" where the language inflects it, the
bare country name where it does not.
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "index.html")

NAMES = {
    "ar":  (u"الجورجية", u"البلغارية"),
    "arc": (u"ܓܘܪܓܝܐ", u"ܒܘܠܓܪܝܐ"),
    "bn":  (u"জর্জীয়", u"বুলগেরীয়"),
    "de":  (u"Georgisch", u"Bulgarisch"),
    "el":  (u"Γεωργιανή", u"Βουλγαρική"),
    "en":  (u"Georgian", u"Bulgarian"),
    "es":  (u"Georgiana", u"Búlgara"),
    "fr":  (u"Géorgien", u"Bulgare"),
    "hi":  (u"जॉर्जियाई", u"बुल्गारियाई"),
    "hy":  (u"Վրացական", u"Բուլղարական"),
    "it":  (u"Georgiano", u"Bulgaro"),
    "ja":  (u"ジョージア", u"ブルガリア"),
    "ka":  (u"ქართული", u"ბულგარული"),
    "ko":  (u"조지아", u"불가리아"),
    "pt":  (u"Georgiano", u"Búlgaro"),
    "ro":  (u"Georgiană", u"Bulgară"),
    "ru":  (u"Грузинская", u"Болгарская"),
    "sr":  (u"Грузијска", u"Бугарска"),
    "sw":  (u"Kijojia", u"Kibulgaria"),
    "uk":  (u"Грузинська", u"Болгарська"),
    "ur":  (u"جارجیائی", u"بلغاریائی"),
    "zh":  (u"格鲁吉亚", u"保加利亚"),
}


def main():
    s = io.open(PAGE, encoding="utf-8").read()
    # Each language is a block opening "<lang>":{"days":[ ... and carrying
    # exactly one jz_greek. The two new keys sort just before it, which is
    # also where the object keeps them.
    blocks = list(re.finditer(r'"([a-z]{2,3})":\{"days":\[', s))
    if len(blocks) != len(NAMES):
        print("expected %d language blocks, found %d" % (len(NAMES), len(blocks)))
        return 1
    if '"jz_georgian":"' in s:
        print("the two Churches are already named; nothing to do")
        return 0

    ends = [b.start() for b in blocks[1:]] + [len(s)]
    done = []
    for b, end in reversed(list(zip(blocks, ends))):
        lang = b.group(1)
        if lang not in NAMES:
            print("unknown language block %r" % lang)
            return 1
        hit = re.search(r'"jz_greek":"', s[b.start():end])
        if not hit:
            print("%s has no jz_greek" % lang)
            return 1
        at = b.start() + hit.start()
        geo, bul = NAMES[lang]
        s = s[:at] + '"jz_bulgarian":"%s","jz_georgian":"%s",' % (bul, geo) + s[at:]
        done.append(lang)

    io.open(PAGE, "w", encoding="utf-8").write(s)
    print("named the Georgian and Bulgarian Churches in %d languages: %s"
          % (len(done), " ".join(sorted(done))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
