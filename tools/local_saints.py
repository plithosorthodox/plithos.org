# -*- coding: utf-8 -*-
"""The Churches' own saints, from the Churches' own calendars.

Ten Churches shared twenty-nine commemorations between them, which is why
they read as one calendar with a different label. The Church of Romania has
canonised dozens since 1955 and had four here; the Church of Serbia her own
line of archbishops, kings and new martyrs, and had six.

Every line below is read off a published list and nothing is inferred. Where
a saint is already on the base calendar he is not repeated: the additions
were checked against SYNAXARION before being written, and the ones that were
already there were dropped.

Sources:

  Romania - the Romanian Patriarchate's own news agency, Basilica, "Sfinţilor
  romani, rugati-va pentru noi", which prints the canonised saints of the
  Romanian Church with the day of each commemoration. The Romanian Church
  keeps the new calendar, and the dates are given as she prints them.

  Serbia - the calendar of the Serbian Orthodox Church. She keeps the old
  reckoning, and every date here is the Julian one, which is the reckoning
  the entries already on the site use: St Sava on 14 January, St Simeon on
  13 February, St Basil of Ostrog on 29 April, the Great Martyr Lazar on 15
  June.

    python3 tools/local_saints.py --check
    python3 tools/local_saints.py --write
"""
import io, json, subprocess, sys

PATH = "index.html"
DECL = "const LOCAL_FIXED="

ADD = {
 "romanian": [
  (1, 10,  u"St Antipa of Calapodești"),
  (4, 14,  u"St Pahomie of Gledin, Bishop of Roman"),
  (4, 24,  u"Ss Ilie Iorest, Sava Brancovici and Simion Ștefan, Metropolitans of Transylvania"),
  (5, 3,   u"St Irodion of Lainici"),
  (5, 12,  u"St John the Wallachian, Martyr"),
  (5, 15,  u"St Iacob Putneanul, Metropolitan of Moldavia"),
  (6, 22,  u"St Grigorie Dascălul, Metropolitan of Wallachia"),
  (6, 30,  u"St Ghelasie of Râmeț"),
  (7, 1,   u"St Leontie of Rădăuți"),
  (7, 26,  u"St Ioanichie the New of Muscel"),
  (8, 5,   u"St Ioan Iacob of Neamț"),
  (8, 7,   u"St Teodora of Sihla"),
  (8, 16,  u"The Brâncoveanu Martyrs: Prince Constantin and his four sons"),
  (9, 15,  u"St Iosif the New of Partoș, Metropolitan of Banat"),
  (9, 26,  u"St Neagoe Basarab, Voivode of Wallachia"),
  (9, 27,  u"St Antim Ivireanul, Hieromartyr, Metropolitan of Wallachia"),
  (10, 28, u"St Iachint, Metropolitan of Wallachia"),
  (11, 30, u"St Andrei Șaguna, Metropolitan of Transylvania"),
  (12, 3,  u"St Gheorghe of Cernica"),
  (12, 13, u"St Dosoftei, Metropolitan of Moldavia"),
  (12, 18, u"St Daniil the Hesychast"),
  (12, 26, u"St Nicodim of Tismana"),
 ],
 "serbian": [
  (1, 15,  u"St Gabriel of Lesnovo"),
  (5, 22,  u"St Jovan Vladimir, Prince of Serbia"),
  (6, 5,   u"St Petar of Koriša"),
  (6, 15,  u"St Jefrem, Patriarch of Serbia"),
  (7, 30,  u"St Angelina of Serbia"),
  (8, 31,  u"The New Martyrs of Jasenovac"),
  (9, 24,  u"St Stefan Vladislav, King of Serbia"),
  (10, 18, u"St Petar of Cetinje, Wonderworker"),
  (10, 19, u"St Prohor of Pčinja"),
  (10, 28, u"St Arsenije of Srem, Archbishop of Serbia"),
  (10, 30, u"St Milutin the King and St Jelena the Queen of Serbia"),
  (11, 11, u"St Stefan Dečanski, King of Serbia"),
  (11, 17, u"St Sebastian of Jackson"),
  (12, 2,  u"St Joanikije of Devič"),
  (12, 20, u"St Danilo II, Archbishop of Serbia"),
 ],
}


def read_table(src, decl):
    i = src.index(decl)
    k = i + len(decl)
    while src[k] not in "{[":
        k += 1
    a, d, instr, q, esc = k, 0, False, "", False
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
                break
        k += 1
    io.open("/tmp/lf.js", "w", encoding="utf-8").write(
        u"require('fs').writeFileSync('/tmp/lf.json',JSON.stringify(%s));" % src[a:k + 1])
    subprocess.check_call(["node", "/tmp/lf.js"])
    return a, k + 1, json.load(io.open("/tmp/lf.json", encoding="utf-8"))


def main():
    src = io.open(PATH, encoding="utf-8").read()
    a, b, table = read_table(src, DECL)

    n = 0
    for juris, rows in ADD.items():
        have = table.setdefault(juris, [])
        seen = set((e["mo"], e["da"], e["name"]) for e in have)
        for mo, da, name in rows:
            if (mo, da, name) in seen:
                continue
            have.append({"mo": mo, "da": da, "name": name})
            n += 1
        have.sort(key=lambda e: (e["mo"], e["da"], e["name"]))

    counts = " ".join("%s:%d" % (k, len(v)) for k, v in sorted(table.items()))
    out = src[:a] + json.dumps(table, ensure_ascii=False, separators=(",", ":")) + src[b:]
    if "--write" in sys.argv:
        io.open(PATH, "w", encoding="utf-8").write(out)
        print("wrote %s: %d added\n  %s" % (PATH, n, counts))
    else:
        print("would add %d\n  %s" % (n, counts))


if __name__ == "__main__":
    main()
