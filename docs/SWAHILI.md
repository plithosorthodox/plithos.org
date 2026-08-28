# Swahili: the register, settled before the writing starts

The thirteenth language, and the first African one. Written, not converted:
the test is whether a reader who prays in Swahili on a Sunday morning in
Nairobi, Dar es Salaam or Kampala would recognise it as something written by
someone from his own Church.

Swahili is not a language being reached for the first time. The Patriarchate
of Alexandria and All Africa has served in it since the nineteen-sixties; the
Divine Liturgy, the Presanctified, the Octoechos and a great deal of the
hymnography are in print in Swahili, and the Church in Kenya, Tanzania and
Uganda is the fastest-growing part of that patriarchate. There is a received
vocabulary. It is not to be improvised.

The danger here is the opposite of the one Japanese carried. Japanese had one
Orthodox register and a mass of Protestant vocabulary that had to be kept out
by knowing the Church's own words. Swahili has an enormous and long-settled
Christian vocabulary that is almost entirely Protestant and Roman Catholic:
a dictionary, a concordance, or the Union Bible will hand it to you fluently
and it will be wrong in the way a fluent thing is wrong. **Padre**, **Bikira
Maria Mtakatifu**, **Bwana Yesu Kristo** as a fixed formula, **misa** - all
good Swahili, none of it this Church's.

## What the Church prints, and where it was read

Before a line of this was written, the Swahili the Church actually sings was
read: the Divine Liturgy and the hymns of the Presanctified as published for
the Swahili-speaking parishes of the Patriarchate of Alexandria, where the
Theotokos is **Mzazi-Mungu**, the Holy Spirit **Roho Mtakatifu**, the Trinity
**Utatu wa asili moja**, the apolytikion **Apolitikio**, and the saints are
named **Mtakatifu Maria wa Misri**, **Mtakatifu Makarios wa Misri**,
**Mtakatifu Yohana Krisostomu**.

## The site has already written a great deal of Swahili

This settles most of the register, and it settles it the way CLAUDE.md says a
register is settled: by reading off what is already printed rather than
deciding afresh.

    data/saint-names.v1.sw.json      1,528 commemorations, in Swahili
    data/glossary-i18n.v1.sw.json    177 terms of the ecclesiastical vocabulary
    data/prayers-i18n.v2.sw.json     100 prayers
    data/rule-i18n.v5.sw.json        the fasting rule
    data/bible.v2.sw.b64             the New Testament
    scripture/sw/                    the Old Testament

Where one of those has decided a word, that word stands. The commemorations
are the important one: it is a Swahili synaxarion index of fifteen hundred
entries, and every rank word below is counted out of it rather than proposed.

## Spelling

Swahili as it is written in Kenya and Tanzania: the Latin alphabet, no
diacritics, no borrowed letters. Hyphens, never dashes. Straight quotes,
never the typographic ones. European numerals.

Swahili has upper case and uses it for names and for the first word of a
sentence. A rank word standing before a name is capitalised the way the
commemorations capitalise it - **Mheshimiwa Sergio wa Radonezh**, **Shahidi
Mkuu Georgi** - and a rank word inside a phrase is not.

## Register

**Swahili allows the plain honorific before a name.** Mtakatifu Nikolao is
right, and the Church's own hymns print Mtakatifu Maria wa Misri. Swahili is
like Greek, Romanian, Serbian and Georgian in this and unlike Russian: the
bare word for holy is not a mark of an English sentence wearing Swahili
words. So `strict` stays False and only the monastic distinction is asserted.

**A monastic is Mheshimiwa, not merely Mtakatifu.** This is the distinction
English does not make at all and the one most often lost. Mheshimiwa is
Swahili for Ὅσιος and преподобный, and the commemorations use it seven
hundred and seventy-three times against Mtakatifu's nine hundred and
sixty-two:

    Mheshimiwa Sergio wa Radonezh          venerable Sergius of Radonezh
    Mheshimiwa Antonio Mkuu                venerable Anthony the Great
    Mheshimiwa Maximo Mkiri                venerable Maximus the Confessor
    Mtakatifu Nikolao wa Mira              St Nicholas of Myra, a hierarch
    Mtakatifu Nabii Eliya                  the holy prophet Elias

## The ranks

Counted from the commemorations. Where two forms are in use there, the count
decides, and the losing form is not written again.

| the order | Swahili | plural |
|---|---|---|
| monastic, venerable | Mheshimiwa | Waheshimiwa |
| monk, ascetic | Mtawa | Watawa |
| martyr | Shahidi | Mashahidi |
| great-martyr | Shahidi Mkuu | Mashahidi Wakuu |
| hieromartyr | Kuhani Shahidi | Makuhani Mashahidi |
| monk-martyr | Shahidi Mtawa | Mashahidi Watawa |
| woman martyr | Shahidi (mwanamke), Bikira Shahidi where a virgin | Mashahidi |
| new martyr | Shahidi Mpya | Mashahidi Wapya |
| passion-bearer | Mbeba-Mateso | Wabeba-Mateso |
| confessor | Mkiri | Wakiri |
| hierarch, bishop | Askofu | Maaskofu |
| archbishop | Askofu Mkuu | Maaskofu Wakuu |
| metropolitan | Metropolita | Metropolita |
| patriarch | Patriaki | Mapatriaki |
| priest | Kasisi | Makasisi |
| deacon | Shemasi | Mashemasi |
| reader | Msomaji | Wasomaji |
| abbot | Abate | Maabate |
| abbess | Abesi | Maabesi |
| apostle | Mtume | Mitume |
| equal-to-the-apostles | Sawa na Mitume | Sawa na Mitume |
| prophet | Nabii | Manabii |
| righteous | Mwenye haki | Wenye haki |
| blessed | Mbarikiwa | Wabarikiwa |
| wonderworker | Mtenda-Miujiza | Watenda-Miujiza |
| unmercenary | Asiyepokea-Malipo | Wasiopokea-Malipo |
| fool-for-Christ | Mpumbavu kwa ajili ya Kristo | Wapumbavu kwa ajili ya Kristo |
| recluse | Aliyejitenga | Waliojitenga |
| stylite | wa Nguzo | wa Nguzo |
| enlightener | Mwangazaji | Waangazaji |
| God-bearer | Mbeba-Mungu | Wabeba-Mungu |
| virgin | Bikira | Mabikira |

**Kuhani Shahidi for the hieromartyr, and nothing else.** The commemorations
carry it a hundred and sixty-nine times, Kasisi Shahidi six times and Shahidi
wa kikuhani four; the majority is the received form and the other two are not
written here. **Metropolita**, not the English Metropolitan, on the same
ground - eighty-nine against seventy-five, and only one of the two is Swahili.

**Abate for the head of a monastery**, because that is what the fifteen
hundred commemorations say. The glossary defines the office under Igumeni,
which is the Greek word the Church also uses; both are real and the
commemorations decide, since the vocabulary stands beside them.

## The Theotokos

**Mzazi-Mungu**, everywhere and without exception. It is what the Church
sings, it is what the glossary defines, and it is the whole point of not
taking the word from a Bible concordance. The site's icon titles say Mama wa
Mungu in places and the older calendar entries let Theotokos stand
untranslated; neither is carried into this vocabulary. One word, and it is
the Church's.

**Bikira Daima Maria** for the Ever-Virgin, **Mama yake Mungu** only where the
English is plainly the descriptive "his Mother" and not the title.

## Noun class, which is where a rendering gives itself away

Almost every rank word above is class 1/2 - the m-/wa- class of persons - and
everything that agrees with it must be in that class. This is the one thing a
non-speaker gets wrong while every word is spelled correctly.

    Mtakatifu huyu, watakatifu hawa          this saint, these saints
    Mtawa aliyeishi, watawa walioishi        the monk who lived, the monks who
    Shahidi mkuu, mashahidi wakuu            the great-martyr, the great-martyrs
    Askofu wa Kaisaria, maaskofu wa Kaisaria the bishop of, the bishops of

The genitive particle follows the class of the head noun and not the
possessor: **wa** for classes 1/2 (mtawa wa Misri, watawa wa Misri), **ya**
for class 9/10 (ikoni ya Mzazi-Mungu, masalia ya mtakatifu), **la** for class
5 (kanisa la Ufufuo), **cha** for class 7 (chetezo cha dhahabu), **kwa** in
the locative. The commonest error in a written-by-outsider text is **wa**
everywhere, and it is visible at a glance.

Places and things are not persons: **monasteri ya Klops**, not wa Klops;
**masalia ya shahidi**, not wa shahidi; **sikukuu ya Bishara**.

## Names

Greek and Slavic saints take the forms the commemorations already give them,
and those are not re-rendered from the English:

    Yohane      John            Petro       Peter       Paulo    Paul
    Nikolao     Nicholas        Gregorio    Gregory     Basili   Basil
    Kirilo      Cyril           Theodoro    Theodore    Simeoni  Symeon
    Antonio     Anthony         Sergio      Sergius     Makario  Macarius
    Athanasio   Athanasius      Ignatio     Ignatius    Stefano  Stephen
    Yakobo      James, Jacob    Efraimu     Ephraim     Georgi   George
    Demetrio    Demetrius       Konstantino Constantine Maria    Mary

Old Testament names take the forms the Swahili scripture prints - Daudi,
Eliya, Haruni, Ayubu, Musa, Yakobo, Zekaria - and saints keep the forms above
even where the two differ.

Places likewise: **Konstantinopoli**, **Aleksandria**, **Antiokia**,
**Kaisaria**, **Yerusalemu**, **Misri**, **Urusi**, **Palestina**,
**Kapadokia**, **Nikomedia**, **Kilikia**, **Dekapolisi**, **Mlima Athos**,
**Mapango ya Kyiv** for the Kyiv Caves.

## The liturgical vocabulary

From the glossary, which is the Church's own and is not to be paraphrased:

    Liturujia Takatifu          the Divine Liturgy
    Liturujia ya Vipaji Vilivyowekwa Wakfu Kabla   the Presanctified
    Kwaresima Kuu               Great Lent          Mfungo  a fast
    Pasaka                      Pascha              Juma Kuu  Holy Week
    Ortro                       matins              Ibada ya jioni  vespers
    Kesha la usiku kucha        the all-night vigil
    Siri Takatifu               the Mysteries       Komunyo  Communion
    Masalia                     relics              Ikoni  an icon
    Monasteri                   a monastery         utawa  the monastic life
    Shahada Kuu ya utawa        the great schema
    Msalaba                     the Cross           Ufufuo  the Resurrection
    Kuzaliwa                    the Nativity        Kulala  the Dormition
    Bishara                     the Annunciation    Kupaa  the Ascension
    Theofania                   the Theophany       Kugeuka Sura  the Transfiguration
    Ulinzi wa Mzazi-Mungu       the Protection      Kuinuliwa kwa Msalaba  the Exaltation
    Sinaksario                  the synaxarion      Zaburi  the Psalter
    Prosfora, Antidoroni, Koliva, Chetezo, Ubani, Troparioni, Kontakioni

## What this vocabulary is

`tools/saint_terms/sw.py`: ten thousand six hundred and thirty-two short
phrases that stand beside the lives - the icon descriptions, the places, the
ranks, the commemorations and the patronages the index shows. They are
written out plainly, all of them, and factored later or never.
