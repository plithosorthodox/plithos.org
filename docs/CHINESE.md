# Chinese: the register, settled before the writing starts

Chinese is the fourteenth language of the vocabulary. It is written for the
Orthodox of the Chinese-speaking world, and the first thing to say about it
is the thing that will trip a writer on the first line: **there is a
perfectly idiomatic, perfectly wrong Christian Chinese in every reference
work.** 天主, 圣神, 弥额尔, 伯多禄 is Catholic Chinese. 上帝, 耶和华,
米迦勒 is Protestant Chinese. Both are excellent Chinese. Neither is what
this site has already published, and a page written out of a dictionary
announces itself in one word.

So this file proposes nothing. Everything below is read off the Chinese the
repository already carries, with the counts, so that it is a record and not
an opinion.

## The four bodies this is read from

| file | what it settles |
|---|---|
| `data/prayers-i18n.v2.zh.json` | 100 prayers - the liturgical register, and the divine names |
| `data/saint-names.v1.zh.json` | 1,528 commemorations - every rank word and the word order |
| `data/glossary-i18n.v1.zh.json` | 177 ecclesiastical nouns |
| `data/saint-info.v1.zh.json` | 119 calendar entries in modern prose |

**Where they disagree the prayers win**, because they are the Church's own
books and a names table is not. They disagree in three places and all three
are named below: the Holy Spirit, the Theotokos, and the word for God.

## Simplified, and it is not close

Twenty-two characters that differ between the scripts were counted across
all four files - some four thousand lines of published Chinese:

    国 70   学 29   圣 1,649   灵 247   会 117   爱 183   礼 125   体 87
    万 125  无 160  实 39      从 213   东 32    马 247   门 116   开 66
    关 13   为 629  师 19      张 10    义 138

and the traditional form of every one of them - 國學聖靈會愛禮體萬無實從東
馬門開關為師張義 - occurs **zero** times. The vocabulary is written in
simplified characters throughout, and a traditional character anywhere in
this table is a mistake, not a variant.

## The divine names

Counted in `prayers-i18n.v2.zh.json` alone, which is the authority:

| | Chinese | count | the form not used |
|---|---|---|---|
| God | 神 | 322 · 我们的神 79 | 上帝 (56, and 我们的上帝 only 11) |
| Jesus | 耶稣 | 84 | no transliterated form occurs at all |
| Christ | 基督 | 142 | 合利斯托斯 0, 哈利斯托斯 0 |
| Jesus Christ | 耶稣基督 | 81 · 主耶稣基督 71 | |
| the Holy Spirit | 圣灵 | 92 | 圣神 0 |
| the Theotokos | 诞神女 | 45 | 圣母 1 |
| the Most Holy Trinity | 至圣圣三 | 20 | 三位一体 0 |
| the Lord | 主 | 594 | |
| the Master | 主宰 | 47 | |
| Amen | 阿们 | 144 | 阿门 0 |

Three of those need their reasoning written down, because a later writer
will find the other form in a neighbouring file and think it is a variant.

**神, not 上帝.** The prayers address God as 神 in their own voice - 主耶稣
基督，我们的神 - 79 times against 11. 上帝 does occur, but chiefly inside
the psalter and the scripture the prayers quote, which carries the wording
of a Chinese Bible edition; it is quotation, not register. The glossary
writes 上帝 in its own explanations, and the glossary is the weakest of the
four authorities on this question.

**圣灵, not 圣神.** 92 to 0 in the prayers. The glossary writes 圣神 seven
times. The prayers win.

**诞神女, and this is the one to be careful about.** The prayers write
诞神女 45 times and 圣母 once, in a compound where both stand together
(最洁净的圣母、诞神女及卒世童贞玛利亚). The names table is split four ways -
圣母 37, 诞神女 16, 天主之母 11, 生神女 2 - which is drift and not a second
usage, and one of those four (天主之母) is the Catholic form. **This table
writes 诞神女 for both Theotokos and Mother of God**, including in the icon
titles, where the names table's habit of 圣母圣像 is the majority only
because the icon entries are numerous. 诞神女 is the word the Church's own
books say.

Around her, from the prayers: 童贞女 the Virgin, 卒世童贞 ever-virgin,
主母 Lady, 至圣 most holy - 至圣诞神女.

## The honorific is the rank

圣 is not the answer to every saint. The table below is what the 1,528
commemorations already print, with their counts, and the losing forms
beside them.

| order of saint | Chinese | count | not |
|---|---|---|---|
| monastic (ὅσιος, преподобный) | 可敬 | 379 | |
| martyr | 致命者 | 361 entries | 殉道者 (29) |
| woman martyr | 致命女 | 76 | 女致命者 (6) |
| hieromartyr, a bishop | 主教致命者 | 19 | |
| hieromartyr, a priest | 致命司祭 | 7 | 致命圣职人员 (3) |
| great-martyr | 大致命者 | 18 | |
| monastic martyr | 致命修士 | 21 | |
| virgin martyr | 童贞致命女 | 23 | |
| new martyr | 新致命者 / 新致命女 | 13 | |
| protomartyr | 首位致命者 | | |
| confessor | 证道者 | 29 | 宣信者 (6) |
| prophet | 先知 | 34 | |
| apostle | 使徒 | 92 | |
| of the Seventy | 七十门徒 / 七十使徒 | | |
| righteous | 义人 | 24 | 义者 (5) |
| passion-bearer | 受难者 | 5 | |
| unmercenary | 无偿医者 | 3 | 不取酬者 (3) |
| fool-for-Christ | 圣愚 | 7 | 为基督而愚者 (6) |
| equal-to-the-apostles | 与使徒同等 | 15 | |
| wonderworker | 行奇迹者 | 62 | |
| enlightener | 启蒙者 | 6 | 光照者 (4) |
| blessed | 真福 | 17 | |
| stylite | 柱头修士 | 7 | |
| hermit, recluse | 隐士 | 9 | |
| God-bearing | 载神者 | | |
| the Forerunner | 前驱 | 9 | |

The two places the names table is genuinely split, 无偿医者/不取酬者 at 3
against 3 and 圣愚/为基督而愚者 at 7 against 6, are settled here by length:
the shorter form, because these are labels standing in a column beside a
life and not sentences.

And the offices, which in Chinese come **before** the name and **after**
the see:

| office | Chinese |
|---|---|
| bishop | 主教 |
| archbishop | 大主教 |
| metropolitan | 都主教 |
| patriarch | 牧首 |
| pope (of Rome, of Alexandria) | 教宗 |
| abbot | 修道院长 |
| abbess | 女修道院长 |
| archimandrite | 修士大司祭 |
| priest, presbyter | 司祭 |
| elder | 长老 |
| deacon | 执事 |
| reader | 诵经者 |
| monk | 修士 |
| nun | 修女 |
| schemamonk | 大修士品修士 |
| prince | 王公 |
| great prince | 大公 |
| emperor, empress | 皇帝, 皇后 |

### 可敬 takes no particle

可敬 stands directly before the name - 可敬保罗, 可敬谢尔吉 - and the names
table writes it so 379 times. 可敬者 (17) is the form used when the rank
stands alone as a label, or when 圣 follows: 可敬者圣比德. There is no
attributive particle in Chinese and none is invented; 可敬的 is not written.

The same for the martyr ranks, which simply precede the name: 致命者巴西流,
致命女塔蒂亚娜, 大致命者圣乔治.

### 圣 before a bare name is allowed

圣 occurs 721 times in the names table and stands before a name, before a
rank, and before an epithet - 圣乔治, 圣使徒安德烈, 圣证道者巴西尔,
大致命者圣乔治. Chinese does not forbid it, so `strict` is **False** for
Chinese and only the monastic rule is asserted: a monastic saint is
可敬 and not merely 圣.

## Words the four bodies do not carry

The queue reaches epithets and terms that no prayer, no commemoration and
no glossary entry supplies. They are settled here once, from what the site
does carry, so they are not decided twice.

**A bare epithet takes 那位.** The vocabulary already writes 那位守斋者,
那位优伶, 那位阿留申人 for an epithet standing alone in the column, so
the same hand gives 那位大者 for the Great, 那位新者 for the New, and
那位成圣者 for the Sanctified. The name is not supplied to complete the
phrase; the label stands as the index prints it.

**The Melodist is 谱曲者.** The names table writes 谱曲者 once and 圣咏者
once, so the count does not settle it. 圣咏者 is taken by the Psalter -
圣咏集 - and would read as a singer of psalms; 谱曲者 says what Romanos
did, which is to make the melodies the hymns are sung to.

**Homoousios is 同一本体.** No prayer here quotes the Creed's clause, so
the phrase is built from the word the prayers do use for essence, 本体,
and written 与父同一本体.

**The Nativity Fast is 圣诞斋期**, formed on 大斋期, which the vocabulary
writes throughout for Great Lent.

## Word order

Chinese puts every modifier before its head, so an English string reverses
wholesale. The place becomes a 的-genitive, or attaches directly when it is
a see:

    Martyr Basil of Ancyra              安基拉的致命者巴西流
    Bishop of Nicomedia                 尼科米底亚主教
    Abbot of Belozersk                  别洛泽尔斯克修道院长
    Recluse of the Kyiv Near Caves      基辅近洞的隐居者
    Wonderworker of Solovki             索洛夫基行奇迹者

so *rank, name, of place* comes out *place 的 rank name*, and the name is
never moved forward to match the English. Where modifiers stack, the larger
place comes first, exactly as the names table writes it:

    沃洛格达先杰姆斯克修道院长可敬阿塔纳修斯
    塞尔维亚黑山扎霍尔姆斯克主教圣巴西尔

的 is dropped where the phrase is a title compound and kept where it is a
genuine genitive; the names table's own practice is the guide - 安基拉的致
命者 with 的, 尼科米底亚主教 without.

## The names themselves

**Where `saint-names.v1.zh.json` prints a saint, that form is used and not
re-derived.** That is the whole rule, and it settles the cases where the
table itself is split, by the counts:

    Basil        瓦西里      (10, and 大瓦西里 for Basil the Great)  not 巴西流 9, 巴西尔 4
    Theodore     德奥多尔    (德奥多 30)                             not 狄奥多 24
    Theodosius   德奥多西
    Sergius      谢尔吉      (14)                                    not 谢尔盖 1
    John         约翰        (71)
    Peter        彼得        (25)                                    not 伯多禄
    Paul         保罗        (17)                                    not 保禄
    George       乔治        (11)
    Nicholas     尼古拉      (10)
    Gregory      格里高利    (16)                                    not 额我略
    Anthony      安东尼      (18)
    Demetrius    德米特里    (7)
    Alexander    亚历山大    (42)
    Mary         玛利亚      (15)

Michael divides by referent and the table is consistent about it: the
Archangel is 弥额尔 - 总领天使弥额尔 - and a Slav named Mikhail is
米哈伊尔. Where a saint is not in the names table, follow the same hand:
Slavonic-shaped names for the saints of Rus', the received Chinese form for
the Greek and the biblical.

**A Catholic form in the names table loses to the prayers.** Two of the
1,528 headings write 达味 and 若瑟 where every other body writes 大卫 (prayers
24, terms 22, names 8) and 约瑟 (terms 25, names 7, prayers 1). The prayers
are the Church's own books and they decide; the two headings are drift of
the same kind as 天主之母. Leo is 良 throughout, as the terms table writes
圣大良 and 亚美尼亚人良.

**Chrysostom is 金口约安.** The terms table writes it 28 times and the
glossary once, against 金口约翰 in four headings; the prayers are split
3 to 1 the other way, which is not one voice, so the weight of what the
site publishes decides. The unmercenaries are 无偿医者 (names 3, terms
25), not 不取酬者 (names 3).

**For a person who appears in Holy Scripture, the published Scripture
names him.** The names table Latinizes Cornelius the Centurion as
科尔尼利乌斯; the Union Version calls him 哥尼流, and his whole
commemoration is Acts 10, so 哥尼流 is what a life that quotes the
chapter can write. This is the same rule as 腓利门 and 布田 above and it
reaches no further: for a saint who is not in Scripture, the names table
still decides.

**The Chinese Old Testament here is thirty-nine books, and that is a gap.**
`scripture/zh` carries Genesis to Malachi in the Union Version and nothing
else: no Wisdom, Sirach, Tobit, Judith, Baruch or Maccabees. So a life whose
subject stands in one of those books cannot quote the site's own Scripture,
and must narrate instead. Judith is written 犹滴 and Holofernes 何乐弗尼,
which is the form the terms table already publishes for him; the pair matches
the Chinese edition that prints those books. Fixing the edition itself is the
scripture job's, not this one's, but the lack is recorded here so the next
person does not rediscover it mid-sentence.

**The Great Schema is 大袍.** Four headings write 大袍隐修士 for the
schemamonks of the Kyiv caves; two others leave the word in Cyrillic as
大схима, which is not a Chinese form and settles nothing. So a life that
mentions the habit writes 大袍, and never the untranslated form.

**The entry's own heading decides that entry's saint, and nothing else.**
Theodora the empress is 狄奥多拉 in her own heading and so she is written
here, but her husband, who is only mentioned, keeps the 德奥菲卢斯 the lives
and the terms table carry eight times against that heading's 狄奥斐洛. Places
go the same way: Verkhoturye is 韦尔霍图里耶, which the other Simeon heading
and the terms table give four times, not the 上图里耶 of this one; Synnada is
锡纳达 by the same count. The rule is for the saint the entry is about,
because that is the name a reader looks up; for everyone and everywhere else
the site's weight still decides.

**The Scripture rule yields where the site has already settled a form.**
The Protomartyr Stephen is 司提反 in the Union Version and nowhere on this
site: the headings write 斯德望 seven times, the terms table seventeen, the
lives twelve, and 司提反 appears not once in any of them. So he is 斯德望,
and the rule above holds only where the site is silent. Cornelius the
Centurion stays 哥尼流 for the reason already given, that his whole
commemoration is Acts 10 and a life that quotes the chapter cannot spell
him two ways in one paragraph.

**Where the names table and the terms table both print a saint, the names
table still wins.** Martin of Tours is 玛尔定 there (3) and 马丁 in the terms
table (3, with one more in the calendar entries). The rule above is not a
count, so it is not overturned by one; the entry's own heading, 基督向图尔的
圣玛尔定显现, decides it.

**A New Testament name the names table does not carry comes from the
published Scripture, not from the terms table.** `data/bible.v4.zh.b64` is
the Union Version, and it is one of the Church's own books here; the terms
table is not. Three cases were settled that way and are settled once:

    Philemon    腓利门     names table 5, Union Version    not 费肋孟 (terms 6, Catholic)
    Pudens      布田       names table 1, Union Version    not 普登 (terms 1)
    Messiah     弥赛亚     Union Version, terms 2, lives 1 not 默西亚 (terms 5, Catholic)
    Zenas       西纳       Union Version (Titus 3:13)      not in the names table

The three that had a Catholic form running against them are the same trap
named at the foot of this file: 费肋孟, 默西亚 and 伯多禄 all come from
the same shelf, and the terms table carries a handful of them.

**Inside a quotation the edition's own spelling stands.** The Union Version
writes 司提反 for Stephen and 阿尼西谋 for Onesimus; the site's prose writes
斯德望 (names 7, terms 17) and 阿尼西母 (names 2). A verse quoted here is
quoted as the edition prints it, and the sentence around it uses the form
this site publishes. Do not reconcile the two.

Places, likewise, from the table:

    Constantinople   君士坦丁堡 (56)      Kyiv        基辅 (94)
    Rome             罗马 (52)            Jerusalem   耶路撒冷 (13)
    Antioch          安提阿 (27)          Alexandria  亚历山大
    Mount Athos      阿索斯山 (10)        Athos alone 圣山 (7)
    Caves            洞窟                 Near/Far    近洞 / 远洞

A name is joined to a second element with the middle dot ·, as the table
writes it: 狄奥多·斯特拉提拉特, 约翰·卡尔费斯.

## Punctuation, and the one that is forbidden

    、    between items of a list
    ，    between clauses
    。    at the end of a sentence
    （）  parentheses
    ：    before an enumeration
    ·     between the parts of a name
    「」  quotation

The names table writes 「」's job with “ ”, and **those two characters
cannot be used here**: `tools/loop.py` counts U+201C and U+201D among the
house characters and refuses a value carrying either. 「」 is written
instead. No em dash, no en dash, no smart apostrophe, for the same reason.
No Latin letters. Arabic numerals are used for years and dates, as the
names table does - 1072年, （6月11日）.

## The vocabulary the site has already settled

From the glossary, and not to be re-rendered:

    圣髑            relics                  圣像            the icon
    圣像壁          the iconostasis         事奉圣礼        the Divine Liturgy
    晚课            Vespers                 晨课            Matins
    晚堂课          Compline                诸时课          the Hours
    子夜课          the Midnight Office     圣咏集          the Psalter
    赞词            the troparion           集祷曲          the kontakion
    大斋期          Great Lent              受难周          Holy Week
    复活节          Pascha                  诸大节          the Great Feasts
    前节 / 后节     forefeast / afterfeast  节期告结        the leavetaking
    修道院          the monastery           修士司祭        the hieromonk
    修士执事        the hierodeacon         修士大司祭      the archimandrite
    大修士品        the great schema        初学者          the novice
    列圣            the glorification       不朽            incorruption
    追思礼          the panikhida           祈祷礼          the moleben
    静修            hesychasm               成神            theosis
    祭饼            the prosphora           祈祷绳          the prayer rope
    属灵之父        the spiritual father    敬礼            veneration
    三歌经          the Triodion            五旬经          the Pentecostarion

and the three words for a solitary, which the names table keeps apart and
which are easy to run together by ear:

    隐居者      the Recluse     18 in the names table against 3 隐修士
    隐士        the Hermit       9 against 1
    隐修士      the Anchorite

闭关者 is not the site's word and is not used.

and from the names table, the feast vocabulary:

    诞生            the Nativity of a saint     安息        the Dormition, the repose
    进堂            the Entry into the Temple   领报        the Annunciation
    举荣            the Exaltation              主显节      the Theophany
    纪念            the Synaxis                 迁移        the translation of relics
    发现            the uncovering of relics    圣髑        the relics
    总领天使        the archangel               十字架      the Cross

## The register of the phrases themselves

These are labels standing in a column beside a life, not prose. Four kinds
run through the queue and they are not written alike:

| kind | example key | how it is written |
|---|---|---|
| a name fragment | `(Vadim) of Persia` | as the names table would write it, no final stop |
| a place | `Amastris, Paphlagonia` | the received form, 、 between the parts |
| a patronage or a theme | `patient prayer`, `courage before thrones` | a bare noun phrase, modifier first, no final stop |
| an icon description | `A monk in the schema, hands folded in prayer.` | a full sentence in modern Chinese, ending 。 |

The icon sentences keep the English clause order and its participial
stacking - the saint, then what stands behind him, then what rises over him
- and read as modern Chinese, not as the classical register of the prayers.
The prayers are quoted for their nouns and never imitated in their grammar.

Chinese does not mark the plural, so 修士 serves for monk and monks alike;
们 is added only where the English is emphatically a company, as the names
table does in 新致命者及宣信者们.

## What a script can catch

`tools/check_register.py --lang zh` holds the table to one rule: a monastic
saint introduced by a bare 圣 with no rank at all. It cannot see word order,
it cannot see whether a name took the form the names table prints, and it
cannot see 圣神 standing where 圣灵 belongs. Those are read, not checked.

`tools/loop.py` refuses a value carrying a house character, a combining
mark, Greek or Cyrillic letters, or the wrong number of lines.

## The order of work

1. This file.
2. `zh` added to `LANGS` in `tools/check_register.py`, from the rank table
   above.
3. Batches of forty to the end of the queue, committing every two to three
   hundred entries.

## The trap

It is not the ranks; those are a table and a table can be followed. It is
that the wrong word will come to hand first every single time, because it
is the Chinese the language actually uses outside this one Church: 圣母 for
the Theotokos, 圣神 or 圣灵 chosen by ear, 天主 for God, 伯多禄 for Peter,
弥撒 for the Liturgy. Every one of them is a page written by someone who
had not read the books this site has already published.

The second trap is the register drift in the other direction: having read
the prayers, writing the captions in their classical cadence. 因我们圣父的
祈祷 is quoted, not imitated. The lives are modern prose and the vocabulary
that labels them is modern.
