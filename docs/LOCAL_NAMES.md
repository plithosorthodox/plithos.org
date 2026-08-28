# The Churches' own commemorations, in every language

Each Church keeps saints the others do not. The calendar carries a hundred
and twenty-seven of them - St Nikephoros the Leper for the Greeks, St Xenia
of St Petersburg for the Russians, Queen Ketevan for the Georgians, Tsar
Lazar for the Serbs, the Brancoveanu martyrs for the Romanians. Fifteen were
already in the calendar's table of names. The other hundred and twelve were
carried in in English and stayed English, so a Russian reader who chose his
own Church met the whole calendar in Russian and his own Church's saints in
English.

    python3 tools/build_local_names.py --check
    python3 tools/build_local_names.py --check --lang ru

One file to a language:

    tools/local_names/<lang>.py     TEXT = {"<the English name>": "..."}

The key is the English name exactly as the calendar carries it; `--check`
rejects a key the calendar does not have. Write all hundred and twenty-seven,
including the fifteen already translated: the builder skips those, and a
complete file is easier to read than one with holes in it.

## The rule that matters most here

**Most of these saints belong to the language you are writing.** They are not
foreign names to be carried across; they are that Church's own saints, and
their names have a settled form in her books which is not a rendering of the
English at all.

A Georgian writing entry 33 does not transliterate "St Tamar, Queen of
Georgia". He writes what the Georgian Church writes: **წმინდა თამარ მეფე**.
A Serb writing entry 109 writes **Свети Стефан Дечански**, not a Serbian
spelling of "Stefan Dečanski, King of Serbia". A Romanian writing entry 78
writes **Sfântul Antim Ivireanul**. A Ukrainian writing entry 116 writes
**Свята рівноапостольна княгиня Ольга**. A Bulgarian saint in Bulgarian, a
Russian saint in Russian, a Greek saint in Greek: **go and find the received
form, and use it.** Where the saint's own Church is the language you are
writing, a rendering invented from the English is simply wrong, and a reader
of that Church will know it in one word.

The same applies in reverse and is easier to miss. When a Georgian saint is
written in Greek, or a Serbian saint in Arabic, there is often still a
received form - the Greek Church has long known ბიძინა, შალვა და ელიზბარი as
Μπιτζίνας, Σάλβας καὶ Ἐλισβάρ. Look before you invent.

## The honorific is the rank, as everywhere on this site

`tools/check_register.py` does not run over this file, so the discipline has
to be kept by hand. The English here is loose and uses "St" for everyone; do
not follow it into your own language.

- A monastic is **Ὅσιος** in Greek, **преподобный** in Russian,
  **преподобни** in Serbian, **Cuviosul** in Romanian, **ღირსი** in Georgian,
  **克肖者** in Japanese. Not the bare word for holy.
- A bishop or patriarch is **святитель**, **Ἅγιος** with his see,
  **Sfântul Ierarh**, **聖德者**.
- A king or prince is **благоверный** / **кнез** / **კეთილმსახური**;
  Bulgarian and Serbian rulers are **цар**, not "king", where that is what
  their own Church calls them.
- A martyr is **мученик**, **Μάρτυς**, **მოწამე**; a great-martyr
  **великомученик**, **Μεγαλομάρτυς**, **დიდმოწამე**; a hieromartyr
  **священномученик**, **Ἱερομάρτυς**; a new martyr **новомученик**,
  **Νεομάρτυς**.
- "Equal-to-the-Apostles" is **равноапостольный**, **Ἰσαπόστολος**,
  **рівноапостольний**, **მოციქულთასწორი**.
- "Synaxis of All Saints of X" takes each language's received form for a
  synaxis: **Собор всех святых, в земле Русской просиявших** is the Russian
  form and is not a translation of the English words.

Reproduce what the entry says rather than improving it. Entry 12 says Great
Martyr Nicholas of Sofia; write the great-martyr, even where you would have
said new martyr.

## Places

Use the name the language uses, not the English one. Homs is Ἔμεσα in Greek.
Bitola is Μοναστήρι. Tarnovo, Ohrid, Zographou, Rila, Gareji, Mtskheta,
Pochaiv and the Kyiv Caves all have settled forms in each of these languages;
Ukrainian says Київські печери and Russian says Киево-Печерская, and neither
is the other.

## Orthography: match the calendar, not your own preference

The calendar already carries fifteen hundred names in your language. Whatever
it does, do. The trap that has already been fallen into once:

**Greek here is monotonic.** Of the one thousand five hundred and eighty-four
Greek strings the calendar carries, every one is monotonic. A polytonic name
set beside them reads as another hand, however correct it is on its own.
`--check` refuses breathings in Greek for that reason. Write
`Osios Nikiforos o Lepros` as **Όσιος Νικηφόρος ο Λεπρός**, not
Ὅσιος Νικηφόρος ὁ Λεπρός.

Serbian is Cyrillic and ekavian. Georgian is Mkhedruli, never Asomtavruli or
Nuskhuri. Japanese follows docs/JAPANESE.md. Where you are unsure, grep the
existing table for a name near yours and follow it.

## House rules

Hyphens, not em or en dashes. Straight quotes. Keep the parenthetical where
the English has one - `(Vidovdan)`, `(Sedmochislenitsi)`, `(1860)` - since it
is how a reader recognises the day; render the word inside it if the language
has its own form, and leave it as it stands if it does not.

An entry left empty is better than an entry guessed. `--check` reports what
is missing, and missing is a state the builder handles: a name with no
rendering in a language simply keeps the English for that language, which is
where it is today.
