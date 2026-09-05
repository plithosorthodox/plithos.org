# Korean: the register, settled before the writing starts

This is the register document for the Korean vocabulary in
`tools/saint_terms/ko.py`. It was written before the first batch, and it is
read off what this site has already published in Korean rather than proposed
from outside. Every rule below is a count, and the count is given, so that a
later reader can check the arithmetic instead of taking the ruling on trust.

The method is the one that took Georgian, Japanese, Swahili and Armenian to
zero: find the competing forms in the files the site already serves, count
them, and let the larger number decide. Where the count is close the reason
for the choice is written out. Nothing here is settled by ear.

## Whose Korean this is

The Eastern Orthodox synaxarion in Korean. The Orthodox Metropolis of Korea
is under the Ecumenical Patriarchate and has service books of its own, and
those books are what the four Korean files on this site are drawn from. That
matters more here than in most languages, because Korean Protestant Christian
usage is enormous, is what a dictionary and a search will both return first,
and uses a different word for God, a different word for the prophets, and a
different Bible-name tradition. It would crowd out the Orthodox forms in
anything written from memory. So nothing here is written from memory.

Two consequences worth stating at the top, because they are the two places a
Korean Christian vocabulary most often goes wrong:

  - God is 하느님, not 하나님. 409 times in the prayers against zero. 하나님
    is the Protestant form and does not appear anywhere in this site's Korean.
  - The prophet is 예언자, not 선지자. 35 in the names table against zero.
    선지자 is again the Protestant word.

## What the site has already written in Korean

Four bodies, and they are not equal in authority. Where they disagree the
prayers win, because they are the Church's own books; after them the names
table, because it is the largest and it is specifically about how a saint is
named; then the glossary; then the calendar entries.

    data/prayers-i18n.v2.ko.json      100 prayers        67,005 hangul
    data/saint-names.v1.ko.json     1,528 commemorations 25,794 hangul
    data/saint-info.v1.ko.json        119 day panels     14,954 hangul
    data/glossary-i18n.v1.ko.json     177 terms           6,942 hangul

`data/calendar-names.v1.ko.json` is the same body as the names table with the
month headings added, and is not counted separately.

## Script: hangul alone

Hangul, with no hanja in a name or a rank. This is a count, not a preference:

    prayers      67,005 hangul     3 hanja
    names        25,794 hangul     0 hanja
    glossary      6,942 hangul     0 hanja
    calendar      14,954 hangul    0 hanja

All three hanja are in the prayers and all three are disambiguating glosses in
parentheses inside a title or a doctrinal phrase - 소(小)취침경 for Small
Compline, 무시(無始)하신 for the Father without beginning. Not one stands in a
saint's name or a rank. The names table, 1,528 commemorations long, has none
at all.

So: hangul throughout. A hanja gloss in parentheses is permitted only where
the site has already used one for the same word, and no new one is introduced
by this lane.

Latin letters do not appear in a rendering either. The handful in the source
files are inside English keys, not Korean values.

## The four names that had to be settled first

Counted in the prayers, which are the Church's own books.

| | form | count | rejected | count |
|---|---|---|---|---|
| God | 하느님 | 409 | 하나님 | 0 |
| | | | 천주 | 0 |
| Christ | 그리스도 | 142 | 하리스토스 | 0 |
| Jesus | 예수 | 84 | 이수스 | 0 |
| Holy Spirit | 성령 | 88 | 성신 | 4 |
| Theotokos | 하느님의 어머니 | 40 | 성모 | 3 |
| | | | 테오토코스 | 9 |

Korean does not take the Greek form of the Lord's name the way Japanese takes
ハリストス. 그리스도 and 예수 are what the Metropolis prints, 142 and 84 times,
against nothing.

The Theotokos is the one that needs care, because the counts invert between
files. 하느님의 어머니 wins the prayers 40 to 3; 성모 wins the names table 42
to 22. Both are the Church's Korean and neither is wrong. The rule this lane
follows is the one the files themselves follow:

  - 하느님의 어머니 where the phrase is doctrinal or liturgical, and wherever
    the English says Theotokos or Mother of God at length - the Annunciation,
    the Dormition, the Synaxis.
  - 성모 in the short attributive compounds the names table already uses -
    성모 자헌 for the Entry into the Temple, 성모의 탄생 for the Nativity.
  - 테오토코스 is left to the glossary, where it explains the Greek word. It
    does not stand in a saint's name.

지극히 거룩하신 renders Most Holy before either: 지극히 거룩하신 하느님의
어머니의 영면.

A saint is 성 before the name, 성인 for the noun standing alone. 421 instances
of 성 + name in the names table.

## How a foreign saint's name is transcribed

From the Greek or Latin, in the Korean ecclesiastical shape the Metropolis
already uses, and NOT through English. The names table has 1,528 of these
already and the rule is read off them.

**Masculine names in -ος / -us take -오, not -오스.** This is the single most
consequential rule in the document and the count is not close:

    tokens ending -오      379
    tokens ending -오스      21

Worked through the individual names:

    그레고리오 20 / 그레고리오스 0      테오도로 23 / 테오도로스 0
    바실리오  22 / 바실리오스  0      스테파노 14 / 스테파노스 0
    안토니오  16 / 안토니오스  0      마카리오 16 / 마카리오스 0
    아타나시오 12 / 아타나시오스 0      데메트리오 7 / 데메트리오스 0

So Sergius is 세르기오, Nicholas 니콜라오, Photius 포티오, Cyril 키릴로.

The exceptions in the table are few and are kept where the site has already
printed them, on the CLAUDE.md rule that a received form is used and not
re-rendered: 게오르기오스 and 게오르기 for George (the table prints both, 4 and
9), 에우스타티오스, 판텔레이몬, 하랄람보스, 니키타스, 크리소스토모. Where this
lane meets one of those saints it writes what the table writes.

**The biblical names take the received Korean Catholic biblical forms**, which
are what the Metropolis uses and what the names table prints:

    Peter 베드로 21      Paul 바오로 16      John 요한 71
    James 야고보         Andrew 안드레아     Philip 필립보
    Michael 미카엘       Gabriel 가브리엘    Stephen 스테파노
    Mary 마리아          Anna 안나           Joseph 요셉
    Elijah 엘리야        Isaiah 이사야       David 다윗

바오로 for Paul, not 바울 or 바울로. The names table prints 바오로 16 times;
바울 appears once each in the glossary and the calendar entries and is the
Protestant form. The names table governs a saint's name.

**Ephraim is 에프렘.** Three forms are in the published files and the counts
are close enough that the question had to be settled rather than guessed:
에프렘 23 (the terms table 9, the lives 12, the names table 2), 에프라임 19
(the names table 6, the lives 13), and 에브렘 once, in the title the prayers
give the Lenten prayer. The terms table is the authority for a name, and it
prints 시리아인 성 에프렘 and 노비 토르크의 성 에프렘 and 성 에프렘의 기도
without a single 에프라임; so the lives are written with 에프렘 for the Syrian,
for Novy Torg and for Perekop alike. The prayer itself is quoted as the
prayers print it, that being the Church's own book.

**Chariton is 카리톤.** The terms table prints 카리톤 five times, among them
the Old Lavra of Chariton in the Judean desert, and the lives already carried
four; the names table's two commemoration headings print 하리톤 and are the
only place it appears. Nine against two, so the lives are written with
카리톤 for the Confessor of Palestine and for Syanzhemsk alike, and the two
headings are the odd readings, not the rule.

**Slavic names transcribe from the Slavic**, not through the Greek: 블라디미르,
티혼, 세라핌, 조시마, 크세니아, 세르기오 for the Greek Sergius but the Russian
saints keep their own shapes where the table prints them.

**Place names take -의.** 로마의, 카파도키아의, 콘스탄티노폴리스의, 키예프의,
알렉산드리아의, 테살로니키의. Constantinople is 콘스탄티노폴리스 (62), not
콘스탄티노플.

## Word order

Korean puts every modifier before its head, so the whole apparatus of place
and rank stands in front of the name and the name comes last. The shape the
names table uses, 1,528 times:

    [place]의  [rank]  [성]  [name]

    로마의 순교자 타티아나            Martyr Tatiana of Rome
    키프로스의 존경하올 아르카디오      Venerable Arcadius of Cyprus
    미라의 성 니콜라오                St Nicholas of Myra
    니사의 주교 성 그레고리오          Saint Gregory, Bishop of Nyssa
    카파도키아 카이사레아의 순교자 고르디오
                                  Martyr Gordius at Caesarea in Cappadocia

An English trailing apposition - "Bishop of Nyssa", "Abbot of Studion" - moves
to the front and becomes part of the modifier stack. It does not stay behind
the name. This is why the register check's generic pattern is not anchored to
the head of the string for Korean: 성 almost never stands first.

Two or more saints joined by "and" take 와/과: 성 사도 베드로와 바오로.
"and those with him" is 그와 함께한 이들.

## Register: the honorific is the rank

The rank is the honorific, as in every language on this site except English.
Korean does not put 성 in front of everything; it names the order first. The
table below is settled by count in the names table (N), the glossary (G) and
the calendar entries (I). Where a form is unrivalled no rival is printed.

| English | Korean | count | rejected |
|---|---|---|---|
| Venerable, monastic | 존경하올 | N 360 | 존자 10, 성덕 2 |
| Martyr | 순교자 | N 460 | 치명자 0 |
| Woman martyr | 순교녀 | N 22 | 여자 순교자 0 |
| Great-martyr | 대순교자 | N 13+ | |
| Hieromartyr | 사제 순교자 | N 87 | 성직 순교자 2, 순교 사제 4 |
| Confessor | 증거자 | N 40 | 고백자 0 |
| Prophet | 예언자 | N 35 | 선지자 0 |
| Apostle | 사도 | N 93 | |
| Righteous | 의인 (의로운 attrib.) | N 28 / 7 | |
| Equal-to-the-Apostles | 사도와 동등한 자 | N 17 | |
| Hierarch, bishop | 주교 | N 261 | |
| Archbishop | 대주교 | N 28 | |
| Metropolitan | 수도 대주교 | N 18 | 관구장 0 |
| Patriarch | 총대주교 | | |
| Abbot | 수도원장 | N 96 | |
| Archimandrite | 수도대사제 | G | |
| Priest, presbyter | 사제 | N 116 | 신부 0, 장로 0 |
| Deacon | 부제 | N 23 | 보제 0 |
| Reader | 독경자 | N 3 | 독서자 0 |
| Monastic (noun) | 수도자 | N 7, I 22 | 수사 0, 수도승 0 |
| Nun | 수녀 | N 4 | 수도녀 0 |
| Virgin | 동정녀 (동정 attrib.) | | |
| Wonderworker | 기적행자 | N 55 | 기적가 8, 기적자 2 |
| Fool-for-Christ | 그리스도를 위한 바보 | N 7 | 바보 성자 7, 유로디비 0 |
| Unmercenary | 무보수 의사 | N 7 | |
| Passion-bearer | 수난자 | N 4 | 고난자 0 |
| Enlightener | 계몽자 | N 10 | 조명자 0 |
| Ascetic | 고행자 | N 19 | 수덕자 0 |
| Recluse, hermit | 은수자 | N 35 | 은둔자 0, 칩거자 0 |
| Stylite | 주상 고행자 | N 1 | |
| Blessed | 복자 / 복녀 | N 14 / 3 | 축복받은 0 |
| Relics | 유물 | N 70 | 유해 0 |
| Icon | 이콘 | N 40 | 성화 (glossary only), 성상 2 |
| Translation of relics | 유물의 이전 | N | |
| Synaxis | 시낙시스 | N | |
| Repose | 안식 | N | |

Fool-for-Christ is the one genuine tie, 7 against 7. 그리스도를 위한 바보 is
chosen because it is transparent, because it is also the form the calendar
entries use (4 against 0), and because 바보 성자 puts the honorific 성 into a
compound where the rank should carry it.

The monastic is 존경하올, 360 times against 10 and 2. That is the word
`tools/check_register.py` is given as the `ko` monastic pattern, and the rule
it asserts is the same as in every other language: a monastic saint takes the
monastic title and not the bare word for holy.

## Prose register

The calendar entries and the glossary are written in the plain declarative
-다 style of written Korean, not the -습니다 of speech: 수도원의 어른이다,
정결 월요일은 대재의 첫날로, 용서의 주일 다음 날이다. The prayers are in the
high liturgical style with -소서 and -나이다, because they are addressed to
God. This lane writes names and phrases, not sentences, so the question mostly
does not arise; where a phrase must carry a verb it takes the plain written
style of the glossary and not the liturgical one, because the vocabulary
labels a saint and does not pray to him.

## Punctuation

Korean uses the ASCII comma and full stop, and this site's Korean files do
too. The house rule in CLAUDE.md holds: hyphens only, no em or en dashes, and
straight quotes. Where the names table needs a parenthetical it uses the plain
ASCII parentheses: 성 니노(니나), 주님 성탄(성탄절). Middle dot · is used
between two commemorations sharing a day, as the table does: 그리스도의 할례 ·
성 대 바실리오.

Numerals are Arabic: 70인 사도, 7위 성 청년, 1860년의 순교자들, 128명의
순교자.

## What a script can catch

`tools/check_register.py --lang ko` asserts the monastic rule: a saint whose
English rank is monastic must be introduced by 존경하올 and not by 성 alone.
The `ko` entry was written into LANGS before the first batch, not after, which
is the order that took the other languages to zero. `strict` is False, because
성 before a name is ordinary Korean and proves nothing either way, exactly as
in Greek, Romanian, Serbian and Georgian.

`tools/build_saint_terms.py --check` asserts that every rendering belongs to
the phrase it is filed under and that the module still imports.

Neither can tell whether a Korean reader would recognise the sentence. Nothing
mechanical can. What they close is the hole that is closable.

## The trap

The trap in Korean is not the script and not the grammar. It is that the
Protestant vocabulary is larger, better indexed and more familiar than the
Orthodox one, and it will arrive first in any sentence written from memory
rather than read off the files. 하나님 for God, 선지자 for the prophets, 바울
for Paul, 성령 세례, 장로 for the presbyter: every one of them is good Korean
and none of them is what the Metropolis of Korea prints. The counts in this
document exist so that the question never has to be answered from memory.

## The lives: what changes and what does not

`tools/saint_lives/ko.py` was begun after the vocabulary was finished, and
nothing above is re-opened for it. The 10,632 renderings in
`tools/saint_terms/ko.py` have already settled every name, rank, place and
epithet this lane will meet; a form is looked up there and copied, not decided
a second time. Where the terms file and memory disagree, the terms file wins,
because it was itself read off the published books.

Three things the vocabulary did not have to settle, and the lives do.

**Prose style: the plain written -다.** The lives are prose, and the model is
the calendar entries, which are written in the plain declarative style of
written Korean and not the -습니다 of speech or the -나이다 of the prayers:
성 바실리는 배교자 율리아누스 때 살았고 총독 사투르니누스 앞에서 그리스도를
고백하였다. Narrative past is -였다 / -았다 / -었다; a standing fact is -이다.
The prayers' high style is not borrowed here, because a life recounts a saint
and does not address God.

**The opening names the saint the way Korean does.** The rank stands before
the name, as everywhere else in this document, and the life begins with it:
니코메디아의 천삼 순교자는, 크레타의 거룩한 열 순교자는, 존경하올 세르기오는.
A monastic opens with 존경하올, which is what `tools/check_register.py --lang
ko` asserts of the first fourteen words. An English trailing apposition moves
in front of the name in the first sentence exactly as it does in a heading.

**Scripture is quoted, not rendered.** Where a life quotes Holy Scripture the
received Korean text this site publishes stands, taken verbatim from
`data/bible.v4.ko.b64` and not translated afresh. That text is a received
translation with a vocabulary of its own, and inside a quotation its wording
governs even where it differs from the register settled above - the rule in
CLAUDE.md that a received form is used and not re-rendered is the same rule
that put 게오르기오스 and 판텔레이몬 in the names. Outside the quotation
marks the register of this document resumes at once.

**Numbers, dates and centuries** are Arabic, as in the vocabulary: 303년,
4세기, 순교자 2만 명, 열 순교자. A number that the English spells out for
rhetorical weight - one thousand and three, the census of a fidelity - may be
written out in Korean where the sentence turns on it, and is otherwise a
numeral.

**Rulers and persecutors** are looked up in the terms file like everyone else,
and it does not run them all through one rule: it prints 디오클레티아누스,
막시미아누스, 트라야누스, 리키니우스, 아우렐리아누스 with the Latin ending
kept, and 데키오, 율리아노, 콘스탄티노, 네로, 레오 in the shape a saint's name
takes. Both are the published forms and both stand. A ruler the terms file has
never named follows whichever of those two patterns his name shares.

## The calendar entries: two things the vocabulary did not settle

`tools/saint_info/ko.py` is the day panel - three fields, `type`, `life` and
`patron` - and the life is the short one. The prose is the plain written -다
of the published panels in `data/saint-info.v1.ko.json`, exactly as the lives
are, and every name, rank, place and epithet is looked up in
`tools/saint_terms/ko.py` and copied rather than decided again. Two fields
needed a ruling the vocabulary had not been asked for.

**The `type` label takes the settled rank, not the published panels' wording.**
The 119 panels already in `data/saint-info.v1.ko.json` are the lowest of the
four authorities named above, and they show it: Venerable is written there as
공경자 (13), 공경할 만한 성인 (11), 공경받는 성인 (2) and 성덕자 (2), and the
hierarch as 성 주교, 성주교 and 성직자 성인. The names table settles the same
words 360 times against 10 and 2. So a panel written by this lane uses the
register table above - 순교자, 순교자들 for a company, 사도, 주교, 축일 - and
Venerable standing alone as a label is **존경하올 성인**, the adnominal the
table settles followed by the noun this document already names for a saint
standing alone. The century keeps the panels' own shape, 4세기, 기원전 9세기,
연대 미상.

**The `patron` line is one sentence ending 전구를 청한다.** The English gives
two petitions divided by a semicolon; Korean joins the two noun phrases with
와/과 or a comma and puts the frame once at the end, which is the frame the
terms file already prints: 눈을 위하여 그에게 전구를 청한다. So

    Invoked for builders; architects.
    짓는 이와 건축가를 위하여 전구를 청한다.

The two noun phrases are themselves looked up in the terms file, which has
already rendered them.

**Faith, Hope and Love, the daughters of Sophia, are the Korean words for
the virtues: 믿음, 소망, 사랑.** Neither the names table nor the terms file
names them, and their entry says in the same breath that their mother named
them for the three great virtues, which is a sentence that only works if the
names are the virtues. The Greek forms would need a gloss the English does
not carry.

**Caesarea is 카이사레아 and Neocaesarea 네오카이사리아.** The two files
disagree about the first: the terms file writes 카이사리아 and the
commemoration headings 카이사레아, five times against two, and the entries
already written follow the headings. The second is not in dispute - the
terms file writes 네오카이사리아 five times and only one heading says
신카이사레아 - so the two names are spelled apart here, each following
whichever of the two files carries it more.

**A khanate is 칸국, not the 한국 the vocabulary uses once.** The word the
terms file gives for it is the ordinary Korean word for Korea, so a
sentence about the conquered khanate of Kazan would read, in Korean, as a
sentence about a conquered Korea. This is the one place where following
the vocabulary would make the text say something else, and the panels
write 칸국.

**Radonezh is 라도네즈, and the twelve entries that wrote 라도네시 were
corrected.** The terms file writes 라도네즈 thirty-eight times against one,
the commemoration headings 라도네시 seven times against two; the terms file
carries the name forty times to nine, and it is the higher authority besides.
The earlier entries had followed the headings, so the home of Saint Sergius
was spelled one way in the vocabulary the panels draw on and another way in
the panels themselves. It is 라도네즈 throughout.
