# Greek: where the translation stands

Working notes. Not deployed.

## Done

**The saints' lives are finished.** `tools/saint_lives/el.py` holds all 1,456
lives, 386,597 words, and `python3 tools/build_saint_lives.py --check` reports
`el 1456 of 1456`. Russian and Greek are now the two complete languages.

## In progress: the calendar entries

`tools/saint_info/el.py`, merged into `index.html` by
`python3 tools/saint_info_i18n.py --write`. At the time of writing: **186 of
1,456**.

The page already carried 146 Greek entries, written in demotic, while the
index lives are in the older ecclesiastical register. Since the calendar entry
is the opening of the index life, the two have to read as one voice, so those
146 were rewritten rather than left alone. They were exactly the first 146
entries in `SAINT_INFO` order, and they are all now done; everything from the
147th on is new.

### The three fields

`type` and `src` are small closed vocabularies and are generated, not typed:
143 category strings and 7 source lines, mapped once in the scratchpad helper
`gktype.py`. Centuries are given in the Greek manner - `Δ΄ αι.`, `ΙΣΤ΄ αι.`,
`Θ΄ αι. π.Χ.` - not `4ος αι.`. The `type` field is omitted for the fore-,
after- and leavetaking feasts and for the icons and synaxes, exactly where the
Russian omits it, because the English calls them all "Saint" and that is a
slip in the categorising rather than something to carry over.

`life` and `patron` are written by hand.

### The shortcut that is safe, and the one that is not

1,303 of the 1,456 calendar lives are **literal prefixes** of the index life
for the same saint. So the Greek is already written: open the finished Greek
life in `tools/saint_lives/el.py`, find the sentence the English prefix stops
at, and take the Greek down to the matching point. This is fast and it keeps
the two lives identical where they overlap, which is the whole point of the
arrangement.

Cutting the Greek *programmatically* - by counting sentences or characters -
is not safe and was rejected. Greek punctuation does not correspond to English
sentence by sentence, the `·` is used freely in this register, and a mis-cut
produces a truncated or over-long entry that no one would catch. The cut is
made by eye, one entry at a time.

The remaining 153 are not prefixes and are written fresh.

### After a batch

    python3 tools/saint_info_i18n.py --check
    python3 tools/saint_info_i18n.py --write
    python3 tools/stamp_build.py
    python3 tools/check_site.py

`index.html` changes on every batch, so the build has to be stamped every
time or `check_site.py` fails.

## Still to do after that

- The remaining 1,270 calendar entries.
- Then the other nineteen languages, one at a time, completely.
