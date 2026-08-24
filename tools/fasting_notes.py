# -*- coding: utf-8 -*-
"""The lines under the fasting pill, in the languages that have them.

FASTNOTE_I18N is keyed by the English note itself, so rewriting the rule in
tools/fasting_rule.py left every new note falling back to English. This
carries the seven languages that were already there across the renamed keys
and writes the new ones. The remaining languages are the lanes' work.

    python3 tools/fasting_notes.py --write
"""
import io, json, os, subprocess, sys

PATH = "index.html"
DECL = "const FASTNOTE_I18N="

# em dash out, hyphen in: the same note, the house's punctuation
RENAME = {
 u"Cheesefare week — no meat; dairy, eggs and fish are permitted all week.":
   "Cheesefare week - no meat; dairy, eggs and fish are permitted all week.",
 u"Great and Holy Week — the strictest days of the year.":
   "Great and Holy Week - the strictest days of the year.",
}

NEW = {
 "Great and Holy Saturday - the fast is kept until midnight.": {
  "el": u"Μέγα Σάββατο - η νηστεία κρατείται μέχρι τα μεσάνυχτα.",
  "ru": u"Великая Суббота - пост хранится до полуночи.",
  "ro": u"Sâmbăta Mare - postul se ține până la miezul nopții.",
  "uk": u"Велика Субота - піст тримають до півночі.",
  "de": u"Karsamstag - das Fasten wird bis Mitternacht gehalten.",
  "es": u"Sábado Santo - el ayuno se guarda hasta la medianoche.",
  "ar": u"السبت العظيم - يُحفظ الصوم حتى منتصف الليل."},
 "Palm Sunday - fish is given.": {
  "el": u"Κυριακή των Βαΐων - επιτρέπεται το ψάρι.",
  "ru": u"Вербное воскресенье - разрешается рыба.",
  "ro": u"Duminica Floriilor - se îngăduie peștele.",
  "uk": u"Вербна неділя - дозволяється риба.",
  "de": u"Palmsonntag - Fisch ist erlaubt.",
  "es": u"Domingo de Ramos - se permite el pescado.",
  "ar": u"أحد الشعانين - يُسمح بالسمك."},
 "Lazarus Saturday - wine and oil are given.": {
  "el": u"Σάββατο του Λαζάρου - επιτρέπονται οίνος και έλαιον.",
  "ru": u"Лазарева суббота - разрешаются вино и елей.",
  "ro": u"Sâmbăta lui Lazăr - se îngăduie vinul și untdelemnul.",
  "uk": u"Лазарева субота - дозволяються вино та олія.",
  "de": u"Lazarus-Samstag - Wein und Öl sind erlaubt.",
  "es": u"Sábado de Lázaro - se permiten el vino y el aceite.",
  "ar": u"سبت لعازر - يُسمح بالخمر والزيت."},
 "The Annunciation - fish is given even in Lent.": {
  "el": u"Ο Ευαγγελισμός - επιτρέπεται το ψάρι ακόμη και μέσα στη Σαρακοστή.",
  "ru": u"Благовещение - рыба разрешается даже Великим постом.",
  "ro": u"Buna Vestire - peștele este îngăduit chiar și în Postul Mare.",
  "uk": u"Благовіщення - рибу дозволяють навіть у Великий піст.",
  "de": u"Mariä Verkündigung - Fisch ist auch in der Großen Fastenzeit erlaubt.",
  "es": u"La Anunciación - se permite el pescado incluso en la Gran Cuaresma.",
  "ar": u"البشارة - يُسمح بالسمك حتى في الصوم الكبير."},
 "Great Lent - wine and oil on Saturdays and Sundays.": {
  "el": u"Μεγάλη Σαρακοστή - οίνος και έλαιον τα Σάββατα και τις Κυριακές.",
  "ru": u"Великий пост - вино и елей по субботам и воскресеньям.",
  "ro": u"Postul Mare - vin și untdelemn sâmbăta și duminica.",
  "uk": u"Великий піст - вино та олія в суботи й неділі.",
  "de": u"Die Große Fastenzeit - Wein und Öl an Samstagen und Sonntagen.",
  "es": u"La Gran Cuaresma - vino y aceite los sábados y domingos.",
  "ar": u"الصوم الكبير - الخمر والزيت في السبوت والآحاد."},
 "The Entry of the Theotokos into the Temple - fish is given.": {
  "el": u"Τα Εισόδια της Θεοτόκου - επιτρέπεται το ψάρι.",
  "ru": u"Введение во храм Пресвятой Богородицы - разрешается рыба.",
  "ro": u"Intrarea în Biserică a Maicii Domnului - se îngăduie peștele.",
  "uk": u"Введення в храм Пресвятої Богородиці - дозволяється риба.",
  "de": u"Der Einzug der Gottesmutter in den Tempel - Fisch ist erlaubt.",
  "es": u"La Entrada de la Theotokos en el Templo - se permite el pescado.",
  "ar": u"دخول والدة الإله إلى الهيكل - يُسمح بالسمك."},
 "The Nativity Fast. The last days before the feast are kept strictly.": {
  "el": u"Νηστεία των Χριστουγέννων. Οι τελευταίες ημέρες πριν από την εορτή κρατούνται αυστηρά.",
  "ru": u"Рождественский пост. Последние дни перед праздником хранятся строго.",
  "ro": u"Postul Nașterii Domnului. Zilele din urmă dinaintea praznicului se țin cu asprime.",
  "uk": u"Різдвяний піст. Останні дні перед святом тримають суворо.",
  "de": u"Die Weihnachtsfastenzeit. Die letzten Tage vor dem Fest werden streng gehalten.",
  "es": u"El Ayuno de la Natividad. Los últimos días antes de la fiesta se guardan con rigor.",
  "ar": u"صوم الميلاد. تُحفظ الأيام الأخيرة قبل العيد بشدة."},
 "The Nativity Fast. In Greek usage fish is given on every day but Wednesday and Friday until Dec 17.": {
  "el": u"Νηστεία των Χριστουγέννων. Κατά την ελληνική τάξη επιτρέπεται το ψάρι κάθε ημέρα εκτός Τετάρτης και Παρασκευής έως τις 17 Δεκεμβρίου.",
  "ru": u"Рождественский пост. По греческому уставу рыба разрешается во все дни, кроме среды и пятницы, до 17 декабря.",
  "ro": u"Postul Nașterii Domnului. După rânduiala grecească, peștele este îngăduit în toate zilele afară de miercuri și vineri, până la 17 decembrie.",
  "uk": u"Різдвяний піст. За грецьким уставом рибу дозволяють в усі дні, крім середи та п'ятниці, до 17 грудня.",
  "de": u"Die Weihnachtsfastenzeit. Nach griechischem Brauch ist Fisch an allen Tagen außer Mittwoch und Freitag bis zum 17. Dezember erlaubt.",
  "es": u"El Ayuno de la Natividad. Según el uso griego se permite el pescado todos los días salvo miércoles y viernes hasta el 17 de diciembre.",
  "ar": u"صوم الميلاد. بحسب العادة اليونانية يُسمح بالسمك كل يوم ما عدا الأربعاء والجمعة حتى 17 كانون الأول."},
 "The Nativity Fast. From Dec 20 no fish is given, whatever the day.": {
  "el": u"Νηστεία των Χριστουγέννων. Από τις 20 Δεκεμβρίου δεν επιτρέπεται ψάρι, όποια ημέρα κι αν είναι.",
  "ru": u"Рождественский пост. С 20 декабря рыба не разрешается ни в какой день.",
  "ro": u"Postul Nașterii Domnului. De la 20 decembrie nu se mai îngăduie pește, în orice zi ar fi.",
  "uk": u"Різдвяний піст. Від 20 грудня риби не дозволяють у жодний день.",
  "de": u"Die Weihnachtsfastenzeit. Ab dem 20. Dezember ist Fisch an keinem Tag erlaubt.",
  "es": u"El Ayuno de la Natividad. Desde el 20 de diciembre no se permite pescado en ningún día.",
  "ar": u"صوم الميلاد. من 20 كانون الأول لا يُسمح بالسمك في أي يوم."},
 "The Nativity Fast. Fish on Saturdays and Sundays; wine and oil on Tuesdays and Thursdays.": {
  "el": u"Νηστεία των Χριστουγέννων. Ψάρι τα Σάββατα και τις Κυριακές· οίνος και έλαιον τις Τρίτες και τις Πέμπτες.",
  "ru": u"Рождественский пост. Рыба по субботам и воскресеньям, вино и елей по вторникам и четвергам.",
  "ro": u"Postul Nașterii Domnului. Pește sâmbăta și duminica; vin și untdelemn marțea și joia.",
  "uk": u"Різдвяний піст. Риба в суботи й неділі, вино та олія у вівторки й четверги.",
  "de": u"Die Weihnachtsfastenzeit. Fisch an Samstagen und Sonntagen; Wein und Öl an Dienstagen und Donnerstagen.",
  "es": u"El Ayuno de la Natividad. Pescado los sábados y domingos; vino y aceite los martes y jueves.",
  "ar": u"صوم الميلاد. السمك في السبوت والآحاد، والخمر والزيت في الثلاثاء والخميس."},
 "The Transfiguration - the one day of the Dormition Fast on which fish is given.": {
  "el": u"Η Μεταμόρφωση - η μόνη ημέρα του Δεκαπενταυγούστου κατά την οποία επιτρέπεται το ψάρι.",
  "ru": u"Преображение - единственный день Успенского поста, когда разрешается рыба.",
  "ro": u"Schimbarea la Față - singura zi a Postului Adormirii în care se îngăduie peștele.",
  "uk": u"Преображення - єдиний день Успенського посту, коли дозволяється риба.",
  "de": u"Die Verklärung - der einzige Tag der Entschlafungsfastenzeit, an dem Fisch erlaubt ist.",
  "es": u"La Transfiguración - el único día del Ayuno de la Dormición en que se permite el pescado.",
  "ar": u"التجلي - اليوم الوحيد من صوم الرقاد الذي يُسمح فيه بالسمك."},
 "The Dormition Fast, among the strictest of the year.": {
  "el": u"Νηστεία του Δεκαπενταυγούστου, από τις αυστηρότερες του έτους.",
  "ru": u"Успенский пост, один из самых строгих в году.",
  "ro": u"Postul Adormirii Maicii Domnului, printre cele mai aspre ale anului.",
  "uk": u"Успенський піст, один із найсуворіших у році.",
  "de": u"Die Mariä-Entschlafungs-Fastenzeit, eine der strengsten des Jahres.",
  "es": u"El Ayuno de la Dormición, de los más estrictos del año.",
  "ar": u"صوم رقاد والدة الإله، من أشد أصوام السنة."},
 "The Apostles' Fast. In Greek usage fish is given on every day but Wednesday and Friday.": {
  "el": u"Νηστεία των Αγίων Αποστόλων. Κατά την ελληνική τάξη επιτρέπεται το ψάρι κάθε ημέρα εκτός Τετάρτης και Παρασκευής.",
  "ru": u"Петров пост. По греческому уставу рыба разрешается во все дни, кроме среды и пятницы.",
  "ro": u"Postul Sfinților Apostoli. După rânduiala grecească, peștele este îngăduit în toate zilele afară de miercuri și vineri.",
  "uk": u"Петрів піст. За грецьким уставом рибу дозволяють в усі дні, крім середи та п'ятниці.",
  "de": u"Die Apostelfastenzeit. Nach griechischem Brauch ist Fisch an allen Tagen außer Mittwoch und Freitag erlaubt.",
  "es": u"El Ayuno de los Apóstoles. Según el uso griego se permite el pescado todos los días salvo miércoles y viernes.",
  "ar": u"صوم الرسل. بحسب العادة اليونانية يُسمح بالسمك كل يوم ما عدا الأربعاء والجمعة."},
 "The Apostles' Fast. Fish on Saturdays and Sundays; wine and oil on Tuesdays and Thursdays.": {
  "el": u"Νηστεία των Αγίων Αποστόλων. Ψάρι τα Σάββατα και τις Κυριακές· οίνος και έλαιον τις Τρίτες και τις Πέμπτες.",
  "ru": u"Петров пост. Рыба по субботам и воскресеньям, вино и елей по вторникам и четвергам.",
  "ro": u"Postul Sfinților Apostoli. Pește sâmbăta și duminica; vin și untdelemn marțea și joia.",
  "uk": u"Петрів піст. Риба в суботи й неділі, вино та олія у вівторки й четверги.",
  "de": u"Die Apostelfastenzeit. Fisch an Samstagen und Sonntagen; Wein und Öl an Dienstagen und Donnerstagen.",
  "es": u"El Ayuno de los Apóstoles. Pescado los sábados y domingos; vino y aceite los martes y jueves.",
  "ar": u"صوم الرسل. السمك في السبوت والآحاد، والخمر والزيت في الثلاثاء والخميس."},
 "The Exaltation of the Cross is a strict fast on whatever day it falls.": {
  "el": u"Η Ύψωση του Τιμίου Σταυρού είναι αυστηρή νηστεία, όποια ημέρα κι αν πέσει.",
  "ru": u"Воздвижение Креста Господня - строгий пост, на какой бы день недели оно ни пришлось.",
  "ro": u"Înălțarea Sfintei Cruci este post aspru, în orice zi ar cădea.",
  "uk": u"Воздвиження Хреста Господнього - суворий піст, на який би день не припало.",
  "de": u"Die Kreuzerhöhung ist ein strenges Fasten, auf welchen Tag sie auch fällt.",
  "es": u"La Exaltación de la Cruz es ayuno estricto, cualquiera que sea el día en que caiga.",
  "ar": u"عيد ارتفاع الصليب صوم شديد، في أي يوم وقع."},
 "The Beheading of the Forerunner is a strict fast on whatever day it falls.": {
  "el": u"Η Αποτομή της Κεφαλής του Προδρόμου είναι αυστηρή νηστεία, όποια ημέρα κι αν πέσει.",
  "ru": u"Усекновение главы Иоанна Предтечи - строгий пост, на какой бы день недели оно ни пришлось.",
  "ro": u"Tăierea Capului Sfântului Ioan Botezătorul este post aspru, în orice zi ar cădea.",
  "uk": u"Усікновення глави Іоанна Предтечі - суворий піст, на який би день не припало.",
  "de": u"Die Enthauptung des Vorläufers ist ein strenges Fasten, auf welchen Tag sie auch fällt.",
  "es": u"La Decapitación del Precursor es ayuno estricto, cualquiera que sea el día en que caiga.",
  "ar": u"قطع رأس السابق صوم شديد، في أي يوم وقع."},
 "The eve of Theophany is a strict fast.": {
  "el": u"Η παραμονή των Θεοφανείων είναι αυστηρή νηστεία.",
  "ru": u"Навечерие Богоявления - строгий пост.",
  "ro": u"Ajunul Bobotezei este post aspru.",
  "uk": u"Навечір'я Богоявлення - суворий піст.",
  "de": u"Der Vorabend von Theophanie ist ein strenges Fasten.",
  "es": u"La víspera de la Teofanía es ayuno estricto.",
  "ar": u"عشية الظهور الإلهي صوم شديد."},
 "A Great Feast on a fast day - fish is given.": {
  "el": u"Μεγάλη εορτή σε ημέρα νηστείας - επιτρέπεται το ψάρι.",
  "ru": u"Великий праздник в постный день - разрешается рыба.",
  "ro": u"Praznic împărătesc într-o zi de post - se îngăduie peștele.",
  "uk": u"Велике свято в пісний день - дозволяється риба.",
  "de": u"Ein Hochfest an einem Fasttag - Fisch ist erlaubt.",
  "es": u"Una Gran Fiesta en día de ayuno - se permite el pescado.",
  "ar": u"عيد كبير في يوم صوم - يُسمح بالسمك."},
}


def span(src, i):
    """The object literal that starts at the first brace after i."""
    k = src.index("{", i)
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
        if c in "\"'":
            instr = True
            q = c
            k += 1
            continue
        if c == "{":
            d += 1
        elif c == "}":
            d -= 1
            if d == 0:
                return src.index("{", i), k + 1
        k += 1
    raise SystemExit("FASTNOTE_I18N: unbalanced")


def main():
    src = io.open(PATH, encoding="utf-8").read()
    i = src.index(DECL)
    a, b = span(src, i + len(DECL))
    # the inner keys are bare identifiers, so this is JS and not JSON
    tmp = "/tmp/fastnote.json"
    io.open("/tmp/fastnote.js", "w", encoding="utf-8").write(
        u"require('fs').writeFileSync(%s,JSON.stringify(%s));"
        % (json.dumps(tmp), src[a:b]))
    subprocess.check_call(["node", "/tmp/fastnote.js"])
    table = json.load(io.open(tmp, encoding="utf-8"))

    added = renamed = 0
    for old, new in RENAME.items():
        if old in table and new not in table:
            table[new] = table.pop(old)
            renamed += 1
    for k, v in NEW.items():
        if k not in table:
            table[k] = v
            added += 1

    out = src[:a] + json.dumps(table, ensure_ascii=False, separators=(",", ":")) + src[b:]
    if "--write" in sys.argv:
        io.open(PATH, "w", encoding="utf-8").write(out)
        print("wrote %s: %d renamed, %d added, %d notes" % (PATH, renamed, added, len(table)))
    else:
        print("would rename %d, add %d, leaving %d notes" % (renamed, added, len(table)))


if __name__ == "__main__":
    main()
