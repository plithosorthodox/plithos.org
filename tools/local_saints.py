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

Six were written and taken out again, because the base already carried them
under another spelling and the first check missed the transliteration:
Gerasimos of Kephalonia, whom the base has as Gerasimus of Cephalonia on 20
October; Ephraim of Nea Makri, whom it has as New Martyr Ephraim on 5 May;
Job of Pochaiv on 28 October; Arsenije of Srem on the same day; and Jovan
Vladimir on 22 May, whom the base gives as John-Vladimir, Prince of Bulgaria.
tools/check_site.py now compares every local entry against the base entries
for its day, so the next one is caught before it ships.

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


  Bulgaria - the list of Bulgarian saints kept at OrthodoxWiki, which gives
  the day of each. The Bulgarian Church keeps the new calendar, and her
  published days are menaion days: the entries already on the base agree with
  it exactly - John of Rila on 19 October, George the New of Sofia on 26 May,
  Clement of Ohrid on 25 November.

  Georgia - the Georgian synaxarion as published in English by the Georgian
  Church in Canada, which prints the civil day. Georgia keeps the old
  reckoning, so every date here is that day less thirteen, and the base
  confirms the conversion at three points: Shio of Mgvime is 22 May there and
  9 May here, Queen Shushanik 10 September and 28 August, All Saints of
  Georgia 24 December and 11 December.


  Greece - the modern saints of the Greek Church, each date taken from the act
  that proclaimed him or from the Church's own commemoration: Arsenios of
  Paros on 31 January, Ephraim of Katounakia on 27 February, Nikolaos Planas
  on 2 March, Savvas of Kalymnos on 7 April, Amphilochios of Patmos on 16
  April (canonised by the Ecumenical Patriarchate in 2018), Ephraim of Nea
  Makri on 5 May, Joseph the Hesychast and the repose of Gerasimos of
  Kephalonia on 16 August, Gerasimos again on 20 October where Kephalonia
  keeps his feast, Arsenios of Cappadocia on 10 November, and Iakovos of Evia
  on 22 November (canonised 2017, commemorated on the 22nd).

  Russia - Theophan the Recluse on 10 January, Ignatius Brianchaninov on 30
  April, Ambrose of Optina on 10 October, and the Synaxis of the Optina
  Elders on 11 October, which the Patriarchate of Moscow instituted in 1996.

  Ukraine - Amphilochius of Pochaiv on 29 April, Job of Pochaiv on 28 October,
  and Petro Mohyla, Metropolitan of Kyiv, on 31 December.

  Antioch - the commemorations the Patriarchate of Antioch keeps as her own,
  and the Synaxis of All Saints of Antioch, which her Holy Synod set on the
  second Sunday after Pentecost, a week after All Saints.

    python3 tools/local_saints.py --check
    python3 tools/local_saints.py --write
"""
import io, json, subprocess, sys

PATH = "index.html"
DECL = "const LOCAL_FIXED="
MOVABLE_DECL = "const LOCAL_MOVABLE="

# off 63 is the second Sunday after Pentecost, the Sunday the site already
# uses for the Synaxis of All Saints of Russia, of Ukraine, of Romania and
# of Bulgaria. Antioch's Holy Synod set hers there too.
ADD_MOVABLE = {"antiochian": [(63, u"Synaxis of All Saints of Antioch")]}

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
 "bulgarian": [
  (1, 15,  u"St Gabriel of Lesnovo"),
  (1, 18,  u"St Joachim I, Patriarch of Tarnovo"),
  (1, 20,  u"St Euthymius, Patriarch of Tarnovo"),
  (1, 30,  u"St Peter, King of Bulgaria"),
  (2, 17,  u"St Romanus of Tarnovo"),
  (3, 11,  u"St Sophronius, Bishop of Vratsa"),
  (5, 17,  u"Great Martyr Nicholas of Sofia"),
  (8, 16,  u"St Joachim of Osogovo"),
  (8, 18,  u"Repose of St John of Rila"),
  (8, 21,  u"New Martyr Simeon of Samokov"),
  (9, 22,  u"St Cosmas of Zographou"),
  (10, 10, u"The 26 Martyrs of Zographou"),
  (10, 27, u"St Demetrius of Basarbovo"),
  (11, 3,  u"Venerable Pimen of Zographou"),
  (11, 22, u"Righteous Michael the Soldier of Bulgaria"),
  (11, 27, u"St Theodosius of Tarnovo"),
  (12, 5,  u"St Nektarios the Bulgarian of Bitola"),
  (12, 23, u"St Nahum of Ohrid"),
 ],
 "georgian": [
  (1, 15,  u"Ss Salome of Ujarma and Perozhavra of Sivnia"),
  (1, 18,  u"St Eprem the Lesser, the Philosopher"),
  (3, 3,   u"St Ioane the Catholicos"),
  (3, 12,  u"Holy King Demetre the Devoted"),
  (3, 16,  u"St Ambrosi the Confessor, Catholicos-Patriarch of All Georgia"),
  (4, 24,  u"Venerable David of the Gareji Monastery"),
  (5, 1,   u"St Tamar, Queen of Georgia"),
  (5, 7,   u"Venerable Ioane of Zedazeni and his Twelve Disciples"),
  (5, 13,  u"Venerable Ekvtime of Mount Athos, the Translator"),
  (6, 27,  u"St George the Hagiorite, and Hieromartyr Kirion II, Catholicos-Patriarch"),
  (7, 20,  u"St Ilia the Righteous"),
  (7, 29,  u"Holy Martyr Evstati of Mtskheta"),
  (7, 30,  u"St Tsotne Dadiani the Confessor"),
  (8, 3,   u"St Razhden, Protomartyr of Georgia, and the Nine Kherkheulidze Brothers"),
  (9, 8,   u"Holy Confessors Ioane and Giorgi-Ioane of Betania"),
  (9, 18,  u"Holy Martyrs Bidzina, Shalva and Elizbar"),
  (10, 5,  u"Venerable Grigol of Khandzta"),
  (10, 20, u"St Gabriel of Samtavro, Confessor and Fool for Christ"),
  (11, 30, u"Holy King Vakhtang Gorgasali"),
  (12, 2,  u"St Ise of Tsilkani"),
  (12, 19, u"Venerable Giorgi the Scribe and his brother Saba of Khakhuli"),
 ],
 "greek": [
  (1, 31,  u"St Arsenios of Paros"),
  (2, 27,  u"St Ephraim of Katounakia"),
  (3, 2,   u"St Nikolaos Planas of Athens"),
  (4, 7,   u"St Savvas the New of Kalymnos"),
  (4, 16,  u"St Amphilochios of Patmos"),
  (8, 16,  u"St Joseph the Hesychast"),
  (11, 10, u"St Arsenios of Cappadocia"),
  (11, 22, u"St Iakovos of Evia"),
 ],
 "russian": [
  (1, 10,  u"St Theophan the Recluse"),
  (4, 30,  u"St Ignatius (Brianchaninov), Bishop of the Caucasus"),
  (10, 10, u"St Ambrose of Optina"),
  (10, 11, u"Synaxis of the Optina Elders"),
 ],
 "ukrainian": [
  (4, 29,  u"St Amphilochius of Pochaiv"),
  (12, 31, u"St Petro Mohyla, Metropolitan of Kyiv"),
 ],
 "antiochian": [
  (1, 28,  u"St Isaac the Syrian"),
  (2, 6,   u"Martyr Elian of Homs"),
  (7, 16,  u"Hieromartyrs Nicholas and Habib Khasha of Damascus"),
 ],
 "serbian": [
  (1, 15,  u"St Gabriel of Lesnovo"),
  (6, 5,   u"St Petar of Koriša"),
  (6, 15,  u"St Jefrem, Patriarch of Serbia"),
  (7, 30,  u"St Angelina of Serbia"),
  (8, 31,  u"The New Martyrs of Jasenovac"),
  (9, 24,  u"St Stefan Vladislav, King of Serbia"),
  (10, 18, u"St Petar of Cetinje, Wonderworker"),
  (10, 19, u"St Prohor of Pčinja"),
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

    out = src[:a] + json.dumps(table, ensure_ascii=False, separators=(",", ":")) + src[b:]

    ma, mb, mov = read_table(out, MOVABLE_DECL)
    for juris, rows in ADD_MOVABLE.items():
        have = mov.setdefault(juris, [])
        seen = set((e["off"], e["name"]) for e in have)
        for off, name in rows:
            if (off, name) in seen:
                continue
            have.append({"off": off, "name": name})
            n += 1
    out = out[:ma] + json.dumps(mov, ensure_ascii=False, separators=(",", ":")) + out[mb:]

    counts = " ".join("%s:%d" % (k, len(v)) for k, v in sorted(table.items()))
    if "--write" in sys.argv:
        io.open(PATH, "w", encoding="utf-8").write(out)
        print("wrote %s: %d added\n  %s" % (PATH, n, counts))
    else:
        print("would add %d\n  %s" % (n, counts))


if __name__ == "__main__":
    main()
