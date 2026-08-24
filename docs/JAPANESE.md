# Japanese: the register, settled before the writing starts

Japanese is the eleventh language of the vocabulary and the second of the
standing lanes. It is not a language into which Orthodox words are
translated. It is a language in which they were **settled**, once, by a
named hand: Saint Nicholas of Japan and Nakai Tsugumaro spent thirty years
over the service books, and what they fixed is what the Japanese Orthodox
Church - 日本ハリストス正教会 - has read ever since.

That is why the ordinary Christian Japanese a dictionary gives is wrong
here, and wrong in a way a reader of that Church notices in one word. The
Catholic and Protestant vocabulary is a different vocabulary. Writing
キリスト on this site is not a near miss; it is a sentence from another
Church.

## The site has already written a great deal of Japanese

Four sources in this repository were written before this file, and the
register is read off them rather than proposed here.

| file | what it settles |
|---|---|
| `data/prayers-i18n.v2.ja.json` | the liturgical register itself, in the classical form the service books keep |
| `data/saint-names.v1.ja.json` | 1,528 commemorations - every rank word and the word order |
| `data/saint-info.v1.ja.json` | 119 lives in modern prose, which is the register the vocabulary sits beside |
| `data/glossary-i18n.v1.ja.json` | the ecclesiastical nouns |

Where they disagree the prayers win, because they are the Church's own
books and the names table is not. They disagree in exactly one place and it
is the most important word in the language; see **Hristos, not Christ**
below.

## Two registers, and which one this table is written in

The prayers are in **bungo**, the classical written language the Nikolai
translations keep to this day:

    我等が聖なる父等の祈祷に因りて、主イイスス・ハリストス、我等の神よ、
    我等を憐れみ給へ。

    光栄は父と子と聖神に帰す、今もいつも世々に。

That is 我等 for we, 爾 for thou, 給へ for the imperative, 因りて for
by. It is beautiful and it is not what the lives are written in.

`data/saint-info.v1.ja.json` writes the lives in **modern Japanese**:

    降誕から八日目に、主イイスス・ハリストスは旧約の律法に従って割礼を受け、
    ガブリエルによって告げられたイイススの名を受けた。

**The vocabulary takes its nouns from the service books and its grammar
from the lives.** ハリストス, 生神女, 克肖, 致命者, 聖神 - every one of
those is the Church's settled noun and none of them is negotiable. But the
phrase around them is modern: 受けた, not 受け給へり. A label standing over
a modern paragraph in classical inflections reads as a quotation, not as a
caption.

## Hristos, not Christ

    ハリストス      Christ. Never キリスト.
    イイスス        Jesus. Never イエス.
    主              the Lord.
    神              God.
    聖神            the Holy Spirit. Never 聖霊.
    生神女          the Theotokos - 生神女マリヤ.
    至聖三者        the Most Holy Trinity.
    主宰            the Master.

The prayers carry ハリストス 135 times and キリスト not once; イイスス 82
times and イエス not once. `saint-names.v1.ja.json` is split almost evenly,
11 against 10 and 9 against 2, which is drift and not a second usage. This
table follows the prayers.

The one place キリスト survives legitimately is inside the received phrase
for a fool-for-Christ, where the names table writes both キリストの故の佯狂者
and キリストのための佯狂者. Even there the compact 佯狂者 alone is the
commoner form and is what this table uses.

## Orthography

**Kanji for the ranks and the nouns, katakana for the names.** That split
is the whole of it, and it is not a stylistic preference: it is how the
Church's books look on the page.

    克肖なるセルギイ          rank in kanji, name in katakana
    大致命者ゲオルギイ
    致命女ワルワラ

Hiragana carries the grammar between them - なる, にして, の, と - and
nothing else. No romaji. No Latin letters at all; `tools/loop.py` refuses
Greek and Cyrillic in a Japanese value and would not have to refuse Latin
if none is written.

Japanese punctuation is the Japanese punctuation: 、 and 。 for the comma
and stop, 「」 for quotation, （） for parenthesis, ・ between the parts of
a name, ー for the long vowel. The house rule against em dashes and smart
quotes is a rule about the Latin characters and does not reach these.

## The names, which are Slavonic and not Greek

This is the second thing a reader checks. Saint Nicholas came from Russia
and brought the Slavonic forms with him, so the Japanese Church says
ワシリイ where a modern transliterator would say バシレイオス, and a
modern transliteration is the mark of a page written from outside.

    Basil            ワシリイ           not バシレイオス
    John             イオアン           not ヨハネ
    Gregory          グリゴリイ
    Peter            ペトル             not ペテロ
    Paul             パウェル           not パウロ
    Nicholas         ニコライ
    Sergius          セルギイ
    Seraphim         セラフィム
    Mary             マリヤ             not マリア
    Barbara          ワルワラ
    Alexis           アレクシイ
    Theodore         フェオドル
    Vladimir         ウラジーミル
    Olga             オリガ
    Andrew           アンドレイ
    Euthymius        エフフィミイ
    Ephraim          エフレム
    Maximus          マクシム
    Constantine      コンスタンチン
    Helen            エレナ

Place names follow the same hand:

    Constantinople   コンスタンディヌポリ      (47 against 9 in the names table)
    Jerusalem        エルサレム
    Alexandria       アレクサンドリア
    Antioch          アンティオキア
    Georgia          グルジア
    Russia           ロシア

And the received epithets are received:

    Chrysostom               金口イオアン
    the Theologian           神学者グリゴリイ
    the First-called         最初に召されたる
    the Great                大 - 大ワシリイ, 大アントニイ
    the Man of God           神の人

Where a saint has a Japanese Orthodox form, it is used and not re-derived.
Saint Nicholas of Japan himself is 聖ニコライ; the Church he founded is
日本ハリストス正教会.

## The honorifics are ranks

聖 is not the answer to every saint. The table below is what the 1,528
commemorations already print, with the counts, so it is a record and not a
proposal.

| order of saint | Japanese | in the names table |
|---|---|---|
| monastic (ὅσιος, преподобный) | 克肖なる / 克肖者 | 362 |
| martyr | 致命者 | 272 |
| hieromartyr | 致命神品 | 85 |
| woman martyr | 致命女 | 80 |
| confessor | 宣信者 | 35 |
| prophet | 預言者 | 34 |
| righteous | 義人 | 27 |
| virgin | 童貞 | 26 |
| equal-to-the-apostles | 亜使徒 | 15 |
| fool-for-Christ | 佯狂者 | 14 |
| blessed | 福者 | 17 |
| new martyr | 新致命者 | 13 |
| right-believing (prince) | 信仰篤き | 9 |
| unmercenary | 無報酬者 | 9 |
| great-martyr | 大致命者 | - |
| woman great-martyr | 大致命女 | - |
| protomartyr | 原致命者 | 5 |
| stylite | 柱行者 | 6 |
| recluse, anchorite | 隠修士 | 5 |
| wonderworker | 成神者 | 56 |
| God-bearing | 載神 | - |
| apostle of the Seventy | 七十使徒 | 34 |
| woman monastic | 克肖女 | 1 |

And the hierarchical offices, which in Japanese follow the see rather than
lead the name:

| office | Japanese |
|---|---|
| bishop | 主教 |
| archbishop | 大主教 |
| metropolitan | 府主教 |
| patriarch | 総主教 |
| abbot | 修道院長 |
| priest | 司祭 |
| presbyter, elder | 長老 |
| deacon | 輔祭 |
| monk | 修道士 |
| nun | 修道女 |
| hierarch (as a body) | 主教者 |

### The attributive, which is the thing a writer gets wrong

**克肖 is not a prefix. It is 克肖なる before a name.**

This is the one distinction English does not make at all and the one most
often lost. The names table writes 克肖なる 359 times and 克肖者 15 times,
and the difference is grammatical, not free:

    克肖なるセルギイ          before a name - the attributive なる
    克肖者                    standing alone, as a label
    克肖者セルギイの永眠      heading a genitive chain, where a noun follows
    克肖にして載神なる父      joined to a second attributive with にして

So: **なる when a name follows and the phrase ends there; 者 when the rank
is the whole phrase, or when the name is possessed by something after it.**
Two attributives are joined with にして - 克肖にして載神なる, 大致命者に
して癒し者 - and never simply stacked.

The same holds for 信仰篤き, which is an adjective and keeps its き:
信仰篤き公ロマン, never 信仰篤公ロマン.

The martyr ranks take no particle at all: 致命者マリン, 致命女イリナ,
大致命者ゲオルギイ, 致命神品ニキタ. Neither does 預言者, 義人, 亜使徒,
七十使徒 or 福者.

### 聖 before a bare name is allowed

This is the second editorial decision `check_register.py --scaffold` marks,
and for Japanese the answer is that the language does **not** forbid it.
聖セルギイ, 聖ニコライ, 聖ワルワラ are ordinary Japanese Orthodox usage and
the lives in `saint-info.v1.ja.json` write them constantly. 聖 stands
before a name, before a rank, and before an epithet:

    聖セルギイ
    聖使徒アンドレイ
    聖神学者グリゴリイ
    大致命者聖ゲオルギイ

so `strict` is **False** for Japanese, and only the monastic rule is
asserted. That is the same answer Georgian, Romanian and Greek give and for
the same reason: the honorific is real before a name, and only the monastic
distinction is a thing a script can hold the language to.

## Word order

Japanese puts the modifier first and the head last, and every place phrase
becomes a の-genitive before the noun it modifies. The English order
reverses wholesale.

    Sergius of Radonezh              ラドネジの聖セルギイ
    Bishop of Novgorod               ノヴゴロドの主教
    Recluse of the Kyiv Far Caves    キエフ遠隔洞窟の隠修士
    Abbot of Novy Torg               ノヴィ・トルグの修道院長

So an English string that runs *rank, name, of place* comes out *place の
rank name*, and a string that runs *name, office, of see* comes out *see の
office name*. The name is not moved to the front to match English.

Where two modifiers stack, the larger place comes first:

    シリアのヘリオポリスの大致命女ワルワラ
    キエフ洞窟（遠隔洞窟）の隠修士にしてトゥロフの主教

## The words the site has already settled

From the glossary and the prayers, and not to be re-rendered:

    聖遺物          relics
    聖体礼儀        the Divine Liturgy
    聖障            the iconostasis
    聖像            the icon
    晩課            Vespers
    早課            Matins
    時課            the Hours
    中夜課          the Midnight Office
    讃詞            the troparion
    コンダク        the kontakion
    大形            the great schema
    斎              the fast
    十二大祭        the Twelve Great Feasts
    前祭 / 後祭     forefeast / afterfeast
    聖堂            the church building
    大聖堂          the cathedral
    修道院          the monastery
    洞窟            the caves
    永眠            the repose
    列聖            the glorification
    遺物の移動      the translation of relics
    遺物の発見      the uncovering of relics
    シナクシス      the synaxis
    主日            the Sunday
    庇護            the Protection
    就寝            the Dormition
    降誕            the Nativity
    神現            the Theophany
    進堂            the Entry into the Temple
    福音            the Annunciation, and the Gospel
    携香女          the myrrhbearing women
    前駆            the Forerunner
    大天使          the archangel
    十字架          the Cross
    挙栄            the Exaltation

## What a script can catch

`tools/check_register.py --lang ja` holds the table to one rule: a monastic
saint introduced by the bare 聖 and no rank at all. It cannot see word
order, it cannot see whether a name took its Slavonic form, and it cannot
see キリスト standing where ハリストス belongs. Those are read, not
checked.

`tools/loop.py` refuses a value carrying Greek or Cyrillic letters, a
combining mark, a house character, or the wrong number of lines. It does
not refuse Latin, so no Latin is written.

## The fields, and what each one is

The queue mixes ten kinds of phrase and they do not take the same
treatment.

| field | what it is | how it is written |
|---|---|---|
| `titles` | the honorific and see that follow a name | rank first, see as a の-genitive |
| `icon` | a sentence describing the icon | modern Japanese, the English clause order kept, ending in 。 |
| `related` | a commemoration cross-referenced | as the names table writes it |
| `relics` | where the relics rest | place の noun, plain |
| `patronCauses` | what a saint is invoked for | a noun phrase, the modifier first |
| `patronWork` | who a saint is invoked by | a noun phrase, plural unmarked |
| `patronPlaces` | a place | the received Japanese form |
| `origin`, `place` | a place | the received Japanese form |
| `baptismalName` | a name | katakana, the Slavonic form |
| `rank`, `type`, `attr`, `state` | a single word | the settled noun |

Japanese does not mark the plural, so 修道士 covers monk and monks and
たち is added only where the English is emphatically a company - 
共にいた者たち, 主教者たち.

## The order of work

1. This file.
2. Some vocabulary - the scaffold reads the terms table and refuses a
   language that has not got one.
3. `python3 tools/check_register.py --scaffold --lang ja`, then the two
   editorial decisions above pasted into `LANGS`.
4. Batches to the end of the queue, committing every two to three hundred.

## The trap

The trap in Japanese is not the honorifics; they are a table and a table
can be followed. It is that Japanese has a perfectly good, perfectly
idiomatic, perfectly wrong vocabulary sitting in every dictionary -
キリスト, 聖霊, 聖母, ペテロ, ヨハネ - and it will come to hand first every
single time, because it is the Japanese the language actually uses outside
this one Church. Every one of those words is a page written by someone who
had not read the Church's books.

The second trap is the register drift in the other direction: having
learned 我等 and 給へ from the prayers, writing the captions in them. The
prayers are quoted, not imitated. The lives are modern and the vocabulary
that labels them is modern.
