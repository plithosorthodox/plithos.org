# Serbian

The sixth language. Written, not converted: the test is whether a reader who
grew up in the Serbian Church would recognise it as something written by
someone from his own Church.

## Script and spelling

Serbian Cyrillic, ekavian, as the Serbian Orthodox Church prints it. The
alphabet is its own:

    а б в г д ђ е ж з и ј к л љ м н њ о п р с т ћ у ф х ц ч џ ш

Note what is **not** there: `ё й щ ъ ы ь э ю я`, and the Ukrainian `і ї є ґ`.
Serbian writes `ј` where Russian writes `й` or the iotated vowels, and `љ њ ђ
ћ џ` where Russian writes digraphs and soft signs. A rendering carrying any of
the absent letters is a lapse into Russian or Ukrainian, and `tools/loop.py`
refuses it rather than leaving it for a reader to find.

Hyphens, never dashes. Straight quotes, never the typographic ones.

## Register

Serbian, like Greek and Romanian, allows the plain honorific before a name:
**Свети Никола** is right. So only the monastic distinction is asserted.

A monastic is **преподобни** or **преподобна**, never merely свети. The rest
of the vocabulary the Church uses, and which the honorific should be drawn
from rather than flattened into свети:

| | |
|---|---|
| hierarch, bishop | светитељ |
| monastic | преподобни, преподобна |
| hieromartyr | свештеномученик |
| venerable-martyr | преподобномученик |
| great-martyr | великомученик, великомученица |
| martyr | мученик, мученица |
| new martyr | новомученик, новомученица |
| righteous | праведни, праведна |
| ruler, prince | благоверни, свети кнез |
| confessor | исповедник |
| unmercenary | бесребреник |
| fool-for-Christ | јуродиви, Христа ради јуродиви |
| apostle | апостол |
| prophet | пророк |
| stylite | столпник |
| enlightener | просветитељ |
| wonderworker | чудотворац |

`tools/check_register.py --lang sr` enforces the monastic distinction and
nothing else, once the vocabulary exists to scaffold it from.

## Order

Vocabulary, then grammar, then the lives and the calendar entries:

    python3 tools/loop.py terms sr --next 40
    python3 tools/check_register.py --scaffold --lang sr
    python3 tools/loop.py lives sr --next 6
    python3 tools/loop.py info sr --next 10

The scaffold reads the terms table and derives the rank patterns from it, so
it refuses to run before the vocabulary is there. See `docs/LOOP.md`.

## Places

Serbian declines a place into an adjective for the epithet: Ликијски,
витинијски, солунски, муромски. Capital where it stands for the saint's
whole title, lower case after a rank word - `епископ витинијски`, but
`(Авив) Египатски`. Where a see has a received Serbian form, use it and do
not re-render it from the English.
